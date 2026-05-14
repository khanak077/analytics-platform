from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.api_key import (
    get_api_key,
)
from app.core.database import get_db
from app.models.api_key import APIKey
from app.models.event import Event
from app.schemas.event import (
    BatchEventCreate,
    EventCreate,
)
from app.core.websocket import manager
from app.tasks.event_tasks import process_event

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post("/")
async def ingest_event(
    payload: EventCreate,
    api_key: APIKey = Depends(get_api_key),
    db: AsyncSession = Depends(get_db),
):

    process_event.delay(
        str(api_key.organization_id),
        payload.event_name,
        payload.properties,
        payload.timestamp.isoformat(),
    )

    await manager.broadcast(
        {
            "event": payload.event_name,
            "message": "new_event_received",
        }
    )

    return {
        "message": "Event queued",
    }


@router.post("/batch")
async def ingest_batch_events(
    payload: BatchEventCreate,
    api_key: APIKey = Depends(get_api_key),
    db: AsyncSession = Depends(get_db),
):
    events = [
        Event(
            organization_id=api_key.organization_id,
            event_name=event.event_name,
            properties=event.properties,
            timestamp=event.timestamp,
        )
        for event in payload.events
    ]

    db.add_all(events)

    await db.commit()

    return {
        "message": f"{len(events)} events ingested",
    }