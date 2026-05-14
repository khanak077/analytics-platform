from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Role
from app.models.membership import Membership
from app.models.organization import Organization
from app.models.user import User
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)


class AuthService:
    @staticmethod
    async def register(
        db: AsyncSession,
        email: str,
        password: str,
        organization_name: str,
    ):
        existing_user = await db.scalar(
            select(User).where(User.email == email)
        )

        if existing_user:
            raise ValueError("Email already registered")

        organization = Organization(
            name=organization_name,
        )

        user = User(
            email=email,
            password_hash=hash_password(password),
        )

        db.add(organization)
        db.add(user)

        await db.flush()

        membership = Membership(
            user_id=user.id,
            organization_id=organization.id,
            role=Role.OWNER,
        )

        db.add(membership)

        await db.commit()

        token = create_access_token(
            {
                "sub": str(user.id),
                "org_id": str(organization.id),
                "role": membership.role.value,
            }
        )

        return {
            "access_token": token,
        }

    @staticmethod
    async def login(
        db: AsyncSession,
        email: str,
        password: str,
    ):
        result = await db.execute(
            select(User)
            .options(
                selectinload(User.memberships)
            )
            .where(User.email == email)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError("Invalid credentials")

        membership = user.memberships[0]

        token = create_access_token(
            {
                "sub": str(user.id),
                "org_id": str(
                    membership.organization_id
                ),
                "role": membership.role.value,
            }
        )

        return {
            "access_token": token,
        }