from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import User
from core.schemas import UserCreateS, UserPatchS, UserPutS
from sqlalchemy import delete, select, update

from services.abstract import AbstractService

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class UserService(
    AbstractService[
        UserCreateS,  # Create schema
        UserPatchS | UserPutS,  # Update schema
        User,  # Model
    ]
):
    @staticmethod
    async def create(
        session: AsyncSession,
        user_create: UserCreateS,
    ) -> User | None:
        query = select(User).where(User.email == user_create.email)
        existing_user = (await session.scalars(query)).first()
        if existing_user:
            return None
        user = User(**user_create.model_dump())
        session.add(user)
        await session.commit()
        return user

    @staticmethod
    async def get(
        session: AsyncSession,
        user_id: int,
    ) -> User | None:
        return await session.get(User, user_id)

    @staticmethod
    async def get_all(
        session: AsyncSession,
    ) -> Sequence[User]:
        stmt = select(User).order_by(User.id)
        result = await session.scalars(stmt)
        return result.all()

    @staticmethod
    async def update(
        session: AsyncSession,
        user_id: int,
        user_update: UserPutS | UserPatchS,
    ) -> User | None:
        values = (
            user_update.model_dump()
            if isinstance(user_update, UserPutS)
            else user_update.model_dump(exclude_unset=True, exclude_none=True)
        )
        stmt = update(User).where(User.id == user_id).values(**values).returning(User)

        updated_user = (await session.scalars(stmt)).first()

        if updated_user is None:
            return None

        await session.commit()
        return updated_user

    @staticmethod
    async def delete(
        session: AsyncSession,
        user_id: int,
    ) -> User | None:
        stmt = delete(User).where(User.id == user_id).returning(User)
        deleted_user = (await session.scalars(stmt)).first()
        if deleted_user is None:
            return None
        await session.commit()
        return deleted_user
