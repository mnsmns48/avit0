from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from DB.models import AvitoData


async def write_data(session: AsyncSession, data: dict):
    stmt = insert(AvitoData).values(data)
    await session.execute(stmt)
    await session.commit()
