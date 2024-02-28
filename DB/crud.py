import psycopg2
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from DB.engine import sync_db
from DB.models import Data
import pandas as pd

from config import hidden


async def async_write_data(session: AsyncSession, data: dict):
    stmt = insert(Data).values(data)
    await session.execute(stmt)
    await session.commit()


def create_db():
    conn = psycopg2.connect(dbname='postgres',
                            user=hidden.db_username,
                            password=hidden.db_password,
                            host='localhost',
                            port=5433
                            )
    cursor = conn.cursor()
    conn.autocommit = True
    sql = f"CREATE DATABASE {hidden.db_name}"
    cursor.execute(sql)
    cursor.close()
    print("База данных успешно создана")
    conn.close()


def sync_write_data(session: Session, data: list):
    stmt = insert(Data).values(data)
    session.execute(stmt)
    session.commit()


def out_excel():
    with Session(bind=sync_db.engine) as session:
        query = session.execute(
            select(Data.id,
                   Data.date,
                   Data.location_1,
                   Data.location_2,
                   Data.price,
                   Data.seller,
                   Data.seller_rank,
                   Data.seller_info,
                   Data.title,
                   Data.link,
                   Data.description
                   ).order_by(Data.id))
    result = query.all()
    df = pd.DataFrame(result)
    filename = 'data.xlsx'
    writer = pd.ExcelWriter(filename)
    try:
        df.to_excel(writer, index=False)
    finally:
        writer.close()


def add_support_info(data: dict):
    keys = list(data.get('links').keys())
