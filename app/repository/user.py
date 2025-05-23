from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import delete, or_, select, update

from app.core.models import UserOrm
from app.core.schemas import UserPutS
from app.repository.abstract import AbstractRepository

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.schemas import UserCreateDbS, UserPatchS


class UserRepository(AbstractRepository[UserOrm]):
    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        user_create_db_s: UserCreateDbS,
    ) -> UserOrm:
        user_orm = UserOrm(**user_create_db_s.model_dump())
        session.add(user_orm)
        await session.commit()
        await session.refresh(user_orm)
        return user_orm

    @classmethod
    async def get(cls, session: AsyncSession, user_id: int) -> UserOrm | None:
        user = await session.get(UserOrm, user_id)
        return user

    @classmethod
    async def get_by_filters(
        cls,
        session: AsyncSession,
        **filters: Any,
    ) -> UserOrm | None:
        query = select(UserOrm).filter_by(**filters)
        user = (await session.scalars(query)).first()
        return user

    # @classmethod
    # async def get_by_conditions(
    #     cls,
    #     session: AsyncSession,
    #     to_schema: type[S] | None = None,
    #     *conditions: Any,  # e.g. [UserOrm.username == "Aleksey", User.email == "test@example.com"]
    # ):
    #     query = select(UserOrm).where(*conditions)
    #     user_orm = (await session.scalars(query)).first()
    #     return cls._to_schema_or_orm(orm_obj=user_orm, to_schema=to_schema)
    #

    @classmethod
    async def check_already_exists(
        cls,
        session: AsyncSession,
        username: str,
        email: str,
    ) -> bool:
        query = select(UserOrm).where(or_(UserOrm.username == username, UserOrm.email == email))
        user_orm = (await session.scalars(query)).first()
        return True if user_orm else False

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
    ) -> Sequence[UserOrm]:
        query = select(UserOrm).order_by(UserOrm.id)
        users = (await session.scalars(query)).all()
        return users

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        user_id: int,
        user_update: UserPutS | UserPatchS,
    ) -> UserOrm | None:
        values = (
            user_update.model_dump()
            if isinstance(user_update, UserPutS)
            else user_update.model_dump(exclude_unset=True, exclude_none=True)
        )
        stmt = update(UserOrm).where(UserOrm.id == user_id).values(**values).returning(UserOrm)

        updated_user = (await session.scalars(stmt)).first()

        if updated_user is None:
            return None

        await session.commit()
        return updated_user

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> UserOrm | None:
        stmt = delete(UserOrm).where(UserOrm.id == user_id).returning(UserOrm)
        deleted_user = (await session.scalars(stmt)).first()
        if deleted_user is None:
            return None
        await session.commit()
        return deleted_user
