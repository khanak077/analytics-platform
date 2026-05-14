import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import (
    TimestampMixin,
    UUIDMixin,
)


class Event(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "events"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    event_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    source_type: Mapped[str] = mapped_column(
        String,
        default="api",
    )

    properties: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )