from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from DB.engine import sync_db
from DB.models import AvitoData
import pandas as pd


async def async_write_data(session: AsyncSession, data: dict):
    stmt = insert(AvitoData).values(data)
    await session.execute(stmt)
    await session.commit()


def sync_write_data(session: Session, data: list):
    stmt = insert(AvitoData).values(data).on_conflict_do_nothing(index_elements=[AvitoData.id])
    session.execute(stmt)
    session.commit()


def out_excel():
    with Session(bind=sync_db.engine) as session:
        query = session.execute(select(AvitoData.id, AvitoData.date, AvitoData.price, AvitoData.title,
                                       AvitoData.description, AvitoData.link).order_by(AvitoData.id))
    result = query.all()
    df = pd.DataFrame(result)
    filename = 'data.xlsx'

    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, index=False)
    writer.close()