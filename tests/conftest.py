from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, Final

import pytest
import pytest_asyncio

from src.config import settings
from src.core.db_manager import db_manager
from src.core.models import BaseOrm, UserOrm
from src.utils.types import ModeEnum

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from collections.abc import AsyncGenerator, Generator

    from _pytest.fixtures import SubRequest
    from sqlalchemy.ext.asyncio import AsyncSession

SKIP_MESSAGE_PATTERN = 'Need "--{db}" option with {db} URI to run'
INVALID_URI_PATTERN = "Invalid {db} URI {uri!r}: {err}"

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def mock_users():
    return [
        UserOrm(username="Andrey", email="andrey@example.com"),
        UserOrm(username="Vova", email="vova@example.com"),
    ]


@pytest.fixture(scope="session", autouse=True)
def event_loop(request: SubRequest) -> Generator[AbstractEventLoop, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db(mock_users) -> AsyncGenerator[None, None]:
    assert settings.mode == ModeEnum.TEST
    assert settings.db.url != settings.test.db.url

    async with db_manager.engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)

    async with db_manager.session_factory() as session:
        for mock_user in mock_users:
            session.add(mock_user)
        await session.commit()

    yield

    await db_manager.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with db_manager.session_factory() as session:
        yield session
