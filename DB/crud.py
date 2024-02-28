import psycopg2
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from DB.engine import sync_db
from DB.models import Data, Support
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


def add_support_info(session: Session, data: dict):
    stmt = insert(Support).values(
        region=data.get('region'),
        internet_magazin=data.get('links').get('Интернет-магазины и IT'),
        obschestvennoe_pitanie=data.get('links').get('Общественное питание'),
        proizvodstvo=data.get('links').get('Производство'),
        razvlecheniya=data.get('links').get('Развлечения'),
        selskoe_hozyaystvo=data.get('links').get('Сельское хозяйство'),
        stroitelstvo=data.get('links').get('Строительство'),
        sfera_uslug=data.get('links').get('Сфера услуг'),
        torgovlya=data.get('links').get('Магазины и пункты выдачи заказов'),
        avtomobilnyi_biznes=data.get('links').get('Автобизнес'),
        krasota_i_ukhod=data.get('links').get('Красота и уход'),
        zdorove_i_medicina=data.get('links').get('Стоматология и медицина'),
        gostinicy_i_bazy_otdykha=data.get('links').get('Туризм'),
        drugoe=data.get('links').get('Другое')
    )
    session.execute(stmt)
    session.commit()


def get_links(session: Session, region_id: int) -> dict:
    answer = dict()
    query = select(Support).filter(Support.id == region_id)
    result = session.execute(query)
    result = result.scalars().all()
    for line in result:
        answer.update(line.__dict__)
    answer.pop('_sa_instance_state')
    answer.pop('id')
    return answer
