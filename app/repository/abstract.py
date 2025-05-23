from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.core.models import Base

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository[M: Base](ABC):
    @classmethod
    @abstractmethod
    async def create(cls, session: AsyncSession, *args: Any, **kwargs: Any) -> M:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get(cls, session: AsyncSession, *args: Any, **kwargs: Any) -> M | None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_all(cls, session: AsyncSession, *args: Any, **kwargs: Any) -> Sequence[M]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def update(cls, session: AsyncSession, *args: Any, **kwargs: Any) -> M | None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def delete(cls, session: AsyncSession, *args: Any, **kwargs: Any) -> M | None:
        raise NotImplementedError()
