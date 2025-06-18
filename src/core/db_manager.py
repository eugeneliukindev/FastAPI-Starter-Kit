from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from sqlalchemy import URL, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.utils.types import ModeEnum

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class DatabaseManager:
    def __init__(self, url: str | URL, **engine_kw):
        self.engine: AsyncEngine = create_async_engine(url=url, **engine_kw)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


if settings.mode == ModeEnum.TEST:
    db_url = settings.test.db.url
    engine_kw = {"poolclass": NullPool}
else:
    db_url = settings.db.url
    engine_kw = {
        "echo": settings.db.echo,
        "echo_pool": settings.db.echo_pool,
        "pool_size": settings.db.pool_size,
        "max_overflow": settings.db.max_overflow,
    }

db_manager = DatabaseManager(
    url=db_url,
    **engine_kw,
)
SessionDep = Annotated[
    AsyncSession,
    Depends(db_manager.session_getter),
]
