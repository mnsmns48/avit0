from asyncio import current_task
from contextlib import asynccontextmanager

from pydantic_settings import BaseSettings
from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine, async_sessionmaker

from config import hidden


class Settings(BaseSettings):
    db_url: str = (f"postgresql+driver://{hidden.db_username}:{hidden.db_password}"
                   f"@localhost:{hidden.db_local_port}/{hidden.db_name}")
    db_echo: bool = hidden.db_echo


settings = Settings()


class AsyncDataBase:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url.replace('driver', 'asyncpg'),
            echo=echo,
            poolclass=NullPool
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        try:
            async with session() as s:
                yield s
        finally:
            await session.remove()


class SyncDataBase:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_engine(
            url=url.replace('driver', 'psycopg2'),
            echo=echo)


async_db = AsyncDataBase(settings.db_url, settings.db_echo)
sync_db = SyncDataBase(settings.db_url, settings.db_echo)
