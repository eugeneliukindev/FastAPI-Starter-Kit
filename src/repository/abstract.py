from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pydantic import BaseModel

from src.core.models import BaseOrm

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class AbstractService[
    CS: BaseModel,  # Create schema
    US: BaseModel,  # Update schema
    M: BaseOrm,  # Model
](ABC):
    @staticmethod
    @abstractmethod
    async def create(session: AsyncSession, schema: CS) -> M | None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get(session: AsyncSession, id_: int) -> M | None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get_all(session: AsyncSession) -> Sequence[M]:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def update(session: AsyncSession, id_: int, schema: US) -> M | None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def delete(session: AsyncSession, id_: int) -> BaseOrm | None:
        raise NotImplementedError()
