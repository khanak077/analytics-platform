import asyncio

from app.core.database import AsyncSessionLocal
from app.models.event import Event
from app.core.celery_app import celery
from datetime import datetime


@celery.task
def process_event(
    organization_id,
    event_name,
    properties,
    timestamp,
):
    asyncio.run(
        save_event(
            organization_id,
            event_name,
            properties,
            timestamp,
        )
    )


async def save_event(
    organization_id,
    event_name,
    properties,
    timestamp,
):
    async with AsyncSessionLocal() as db:

        timestamp = datetime.fromisoformat(
            timestamp
        )
        
        event = Event(
            organization_id=organization_id,
            event_name=event_name,
            properties=properties,
            timestamp=timestamp,
        )

        db.add(event)

        await db.commit()