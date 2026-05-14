from pydantic import BaseModel


class DashboardCreate(BaseModel):
    name: str
    description: str | None = None