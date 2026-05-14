from datetime import datetime
from typing import Any

from pydantic import BaseModel


class EventCreate(BaseModel):
    event_name: str
    properties: dict[str, Any]
    timestamp: datetime


class BatchEventCreate(BaseModel):
    events: list[EventCreate]