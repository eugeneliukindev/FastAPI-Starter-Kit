from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import (
    APIRouter,
)

from app.core.schemas import UserCreateS, UserPutS, UserS
from app.core.schemas.user import UserPatchS
from app.exceptions.users import raise_user_already_exists_exp, raise_user_not_found_exp
from app.repository import UserService
from app.utils.types import SessionDep

if TYPE_CHECKING:
    from typing import Any
router = APIRouter(tags=["Users"], prefix="/users")


@router.get("", response_model=list[UserS])
async def get_all_users(
    session: SessionDep,
) -> Any:
    users = await UserService.get_all(session=session)
    return users


@router.post("", response_model=UserS)
async def create_user(
    session: SessionDep,
    user_create: UserCreateS,
) -> Any:
    user = await UserService.create(
        session=session,
        user_create=user_create,
    )
    if user is None:
        raise_user_already_exists_exp()

    return user


@router.get("/{user_id}", response_model=UserS)
async def get_user(
    user_id: int,
    session: SessionDep,
) -> Any:
    user = await UserService.get(session=session, user_id=user_id)
    if user is None:
        raise_user_not_found_exp()
    return user


@router.put("/{user_id}", response_model=UserS)
async def update_user_partial(
    session: SessionDep,
    user_id: int,
    user_put: UserPutS,
) -> Any:
    updated_user = await UserService.update(
        session=session, user_id=user_id, user_update=user_put
    )
    if updated_user is None:
        raise_user_not_found_exp()
    return updated_user


@router.patch("/{user_id}", response_model=UserS)
async def update_user(
    session: SessionDep,
    user_id: int,
    user_patch: UserPatchS,
) -> Any:
    updated_user = await UserService.update(
        session=session,
        user_id=user_id,
        user_update=user_patch,
    )
    if updated_user is None:
        raise_user_not_found_exp()
    return updated_user


@router.delete("/{user_id}", response_model=UserS)
async def delete_user(
    session: SessionDep,
    user_id: int,
) -> Any:
    deleted_user = await UserService.delete(session=session, user_id=user_id)
    if deleted_user is None:
        raise_user_not_found_exp()
    return deleted_user
