import uuid

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.enums import Role


class Membership(Base, TimestampMixin):
    __tablename__ = "memberships"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        primary_key=True,
    )

    role: Mapped[Role] = mapped_column(
        Enum(Role),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="memberships",
    )

    organization = relationship(
        "Organization",
        back_populates="memberships",
    )