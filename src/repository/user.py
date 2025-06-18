from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import delete, select, update

from src.core.models import UserOrm
from src.core.schemas import UserCreateS, UserPatchS, UserPutS
from src.repository.abstract import AbstractService

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class UserService(
    AbstractService[
        UserCreateS,  # Create schema
        UserPatchS | UserPutS,  # Update schema
        UserOrm,  # Model
    ]
):
    @staticmethod
    async def create(
        session: AsyncSession,
        user_create: UserCreateS,
    ) -> UserOrm | None:
        query = select(UserOrm).where(UserOrm.email == user_create.email)
        existing_user = (await session.scalars(query)).first()
        if existing_user:
            return None
        user = UserOrm(**user_create.model_dump())
        session.add(user)
        await session.commit()
        return user

    @staticmethod
    async def get(
        session: AsyncSession,
        user_id: int,
    ) -> UserOrm | None:
        return await session.get(UserOrm, user_id)

    @staticmethod
    async def get_all(
        session: AsyncSession,
    ) -> Sequence[UserOrm]:
        stmt = select(UserOrm).order_by(UserOrm.id)
        result = await session.scalars(stmt)
        return result.all()

    @staticmethod
    async def update(
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

    @staticmethod
    async def delete(
        session: AsyncSession,
        user_id: int,
    ) -> UserOrm | None:
        stmt = delete(UserOrm).where(UserOrm.id == user_id).returning(UserOrm)
        deleted_user = (await session.scalars(stmt)).first()
        if deleted_user is None:
            return None
        await session.commit()
        return deleted_user
