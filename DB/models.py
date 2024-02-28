import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import DateTime, BIGINT, Text

from config import hidden


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Data(Base):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=False))
    location_1: Mapped[Optional[str]]
    location_2: Mapped[Optional[str]]
    price: Mapped[Optional[int]] = mapped_column(BIGINT)
    seller: Mapped[Optional[str]]
    seller_rank: Mapped[Optional[float]]
    seller_info: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    link: Mapped[Optional[str]]


class Support(Base):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    region: Mapped[str]
    internet_magazin: Mapped[str]
    obschestvennoe_pitanie: Mapped[str]
    proizvodstvo: Mapped[str]
    razvlecheniya: Mapped[str]
    selskoe_hozyaystvo: Mapped[str]
    stroitelstvo: Mapped[str]
    sfera_uslug: Mapped[str]
    torgovlya: Mapped[str]
    avtomobilnyi_biznes: Mapped[str]
    krasota_i_ukhod: Mapped[str]
    zdorove_i_medicina: Mapped[str]
    gostinicy_i_bazy_otdykha: Mapped[str]
    drugoe: Mapped[str]
