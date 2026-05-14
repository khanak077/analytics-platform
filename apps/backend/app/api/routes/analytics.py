from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import (
    get_current_user,
)
from app.core.database import get_db
from app.models.event import Event
from app.models.user import User

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/summary")
async def analytics_summary(
    current_user: User = Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(get_db),
):
    membership = current_user.memberships[0]

    total_events_query = await db.execute(
        select(func.count(Event.id)).where(
            Event.organization_id
            == membership.organization_id
        )
    )

    total_events = total_events_query.scalar()

    events_by_name_query = await db.execute(
        select(
            Event.event_name,
            func.count(Event.id),
        )
        .where(
            Event.organization_id
            == membership.organization_id
        )
        .group_by(Event.event_name)
    )

    events_by_name = [
        {
            "event_name": row[0],
            "count": row[1],
        }
        for row in events_by_name_query.all()
    ]

    return {
        "total_events": total_events,
        "events_by_name": events_by_name,
    }