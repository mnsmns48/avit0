import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import DateTime, BIGINT


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Data(Base):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=False))
    region: Mapped[Optional[str]]
    location: Mapped[Optional[str]]
    price: Mapped[Optional[int]] = mapped_column(BIGINT)
    seller: Mapped[Optional[str]]
    seller_rank: Mapped[Optional[float]]
    seller_info: Mapped[Optional[str]]
    category: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    link: Mapped[Optional[str]]


class Support(Base):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    region: Mapped[str]
    franshizy: Mapped[Optional[str]]
    internet_magazin: Mapped[Optional[str]]
    obschestvennoe_pitanie: Mapped[Optional[str]]
    proizvodstvo: Mapped[Optional[str]]
    razvlecheniya: Mapped[Optional[str]]
    selskoe_hozyaystvo: Mapped[Optional[str]]
    stroitelstvo: Mapped[Optional[str]]
    sfera_uslug: Mapped[Optional[str]]
    torgovlya: Mapped[Optional[str]]
    avtomobilnyi_biznes: Mapped[Optional[str]]
    krasota_i_ukhod: Mapped[Optional[str]]
    zdorove_i_medicina: Mapped[Optional[str]]
    gostinicy_i_bazy_otdykha: Mapped[Optional[str]]
    drugoe: Mapped[Optional[str]]
