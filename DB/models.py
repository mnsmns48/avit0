import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import DateTime, BIGINT, Text


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class AvitoData(Base):
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