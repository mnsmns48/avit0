from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from DB.models import AvitoData


async def async_write_data(session: AsyncSession, data: dict):
    stmt = insert(AvitoData).values(data)
    await session.execute(stmt)
    await session.commit()


def sync_write_data(session: Session, data: list):
    stmt = insert(AvitoData).values(data)
    session.execute(stmt)
    session.commit()
