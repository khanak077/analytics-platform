from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import (
    get_current_user,
)
from app.core.database import get_db
from app.core.security import (
    generate_api_key,
    hash_password,
)
from app.models.api_key import APIKey
from app.models.membership import Membership
from app.models.user import User

router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"],
)


@router.post("/")
async def create_api_key(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    membership = current_user.memberships[0]

    raw_key = generate_api_key()

    api_key = APIKey(
        organization_id=membership.organization_id,
        name="Default API Key",
        key_hash=hash_password(raw_key),
    )

    db.add(api_key)

    await db.commit()

    return {
        "api_key": raw_key,
    }