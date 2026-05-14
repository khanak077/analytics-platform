from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.api.routes.auth import router as auth_router
from app.core.database import get_db

from app.api.routes.users import router as users_router

from app.api.routes.api_keys import (
    router as api_keys_router,
)

from app.api.routes.events import (
    router as events_router,
)

from app.api.routes.analytics import (
    router as analytics_router,
)

from app.api.routes.dashboards import (
    router as dashboards_router,
)

from app.api.routes.ws import (
    router as ws_router,
)

app = FastAPI()

app.include_router(auth_router)

app.include_router(users_router)

app.include_router(api_keys_router)

app.include_router(events_router)

app.include_router(analytics_router)

app.include_router(dashboards_router)

app.include_router(ws_router)

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/db-test")
async def db_test(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(text("SELECT 1"))

    return {"database": result.scalar()}