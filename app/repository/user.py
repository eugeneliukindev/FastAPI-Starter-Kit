from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import or_, select

from app.core.models import UserOrm
from app.repository.base import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.schemas import UserCreateDbS, UserPatchS, UserPutS


class UserRepository(BaseRepository[UserOrm, UserCreateDbS, UserPatchS | UserPutS]):
    model_orm = UserOrm

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
