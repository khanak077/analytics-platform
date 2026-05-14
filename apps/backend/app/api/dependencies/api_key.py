from fastapi import Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import verify_password
from app.models.api_key import APIKey


async def get_api_key(
    x_api_key: str = Header(...),
):
    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(APIKey).where(
                APIKey.is_active == True
            )
        )

        api_keys = result.scalars().all()

        for api_key in api_keys:
            if verify_password(
                x_api_key,
                api_key.key_hash,
            ):
                return api_key

    raise HTTPException(
        status_code=401,
        detail="Invalid API key",
    )