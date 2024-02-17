import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import DateTime, BIGINT


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class AvitoData(Base):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=False))
    price: Mapped[Optional[int]] = mapped_column(BIGINT)
    title: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]]
    link: Mapped[str]

