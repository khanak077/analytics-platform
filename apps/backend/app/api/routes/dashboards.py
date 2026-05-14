from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import (
    get_current_user,
)
from app.core.database import get_db
from app.models.dashboard import Dashboard
from app.models.user import User
from app.schemas.dashboard import DashboardCreate

router = APIRouter(
    prefix="/dashboards",
    tags=["Dashboards"],
)


@router.post("/")
async def create_dashboard(
    payload: DashboardCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(get_db),
):
    membership = current_user.memberships[0]

    dashboard = Dashboard(
        organization_id=membership.organization_id,
        name=payload.name,
        description=payload.description,
    )

    db.add(dashboard)

    await db.commit()

    return {
        "message": "Dashboard created",
    }


@router.get("/")
async def list_dashboards(
    current_user: User = Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(get_db),
):
    membership = current_user.memberships[0]

    result = await db.execute(
        select(Dashboard).where(
            Dashboard.organization_id
            == membership.organization_id
        )
    )

    dashboards = result.scalars().all()

    return dashboards