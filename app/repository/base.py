from __future__ import annotations

from typing import TYPE_CHECKING, Literal, overload

from pydantic import BaseModel
from sqlalchemy import delete, select, update

from app.core.models import Base
from app.repository.abstract import AbstractRepository

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.models import Base


class BaseRepository[M: Base, CreateS: BaseModel, UpdateS: BaseModel](AbstractRepository[M]):
    model_orm: type[M]

    @classmethod
    @overload
    async def _execute_query(
        cls, session: AsyncSession, result_method: Literal["first"], **filter_by: Any
    ) -> M | None: ...

    @classmethod
    @overload
    async def _execute_query(
        cls, session: AsyncSession, result_method: Literal["all"], **filter_by: Any
    ) -> Sequence[M]: ...

    @classmethod
    @overload
    async def _execute_query(
        cls, session: AsyncSession, result_method: Literal["one_or_none"], **filter_by: Any
    ) -> M | None: ...

    @classmethod
    @overload
    async def _execute_query(cls, session: AsyncSession, result_method: Literal["one"], **filter_by: Any) -> M: ...

    @classmethod
    async def _execute_query(
        cls,
        session: AsyncSession,
        result_method: Literal["first", "all", "one_or_none", "one"],
        **filter_by: Any,
    ) -> Any:
        query = select(cls.model_orm).filter_by(**filter_by)
        result = await session.scalars(query)
        return getattr(result, result_method)()

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        schema: CreateS,
    ) -> M:
        orm_obj: M = cls.model_orm(**schema.model_dump())
        session.add(orm_obj)
        await session.commit()
        await session.refresh(orm_obj)
        return orm_obj

    @classmethod
    async def find_first(cls, session: AsyncSession, **filter_by: Any) -> M | None:
        return await cls._execute_query(session, "first", **filter_by)

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by: Any) -> Sequence[M]:
        return await cls._execute_query(session, "all", **filter_by)

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by: Any) -> M | None:
        return await cls._execute_query(session, "one_or_none", **filter_by)

    @classmethod
    async def find_one(cls, session: AsyncSession, **filter_by: Any) -> M:
        return await cls._execute_query(session, "one", **filter_by)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        id_: int,
        schema: UpdateS,
    ) -> M | None:
        stmt = (
            update(cls.model_orm)
            .where(cls.model_orm.id == id_)
            .values(**schema.model_dump(exclude_none=True, exclude_unset=True))
            .returning(cls.model_orm)
        )

        updated_orm_obj: M | None = (await session.scalars(stmt)).one_or_none()

        if updated_orm_obj is None:
            return None

        await session.commit()
        return updated_orm_obj

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        id_: int,
    ) -> M | None:
        stmt = delete(cls.model_orm).where(cls.model_orm.id == id_).returning(cls.model_orm.id)
        deleted_orm_obj: M | None = (await session.scalars(stmt)).first()
        if deleted_orm_obj is None:
            return None
        await session.commit()
        return deleted_orm_obj
