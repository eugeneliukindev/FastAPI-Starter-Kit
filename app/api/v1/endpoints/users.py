from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import (
    APIRouter,
)

from app.auth.password import get_password_hash
from app.core.db_manager import SessionDep
from app.core.schemas import UserCreateS, UserPutS, UserS
from app.core.schemas.user import UserCreateDatabaseS, UserPatchS
from app.exceptions.users import user_already_exists_exp, user_not_found_exp
from app.repository import UserRepository

if TYPE_CHECKING:
    from typing import Any
router = APIRouter(tags=["Users"], prefix="/users")


@router.get("", response_model=list[UserS])
async def get_all_users(
    session: SessionDep,
) -> Any:
    users = await UserRepository.get_all(session=session)
    return users


@router.post("", response_model=UserS)
async def create_user(
    session: SessionDep,
    user_create: UserCreateS,
) -> Any:
    hashed_password = get_password_hash(password=user_create.password)
    user_create_db = UserCreateDatabaseS(
        **user_create.model_dump(exclude={"password"}),
        hashed_password=hashed_password,
    )
    user = await UserRepository.create(
        session=session,
        user_create_db=user_create_db,
    )
    if user is None:
        raise user_already_exists_exp

    return user


@router.get("/{user_id}", response_model=UserS)
async def get_user(
    user_id: int,
    session: SessionDep,
) -> Any:
    user = await UserRepository.get(session=session, user_id=user_id)
    if user is None:
        raise user_not_found_exp
    return user


@router.put("/{user_id}", response_model=UserS)
async def update_user_partial(
    session: SessionDep,
    user_id: int,
    user_put: UserPutS,
) -> Any:
    updated_user = await UserRepository.update(
        session=session, user_id=user_id, user_update=user_put
    )
    if updated_user is None:
        raise user_not_found_exp
    return updated_user


@router.patch("/{user_id}", response_model=UserS)
async def update_user(
    session: SessionDep,
    user_id: int,
    user_patch: UserPatchS,
) -> Any:
    updated_user = await UserRepository.update(
        session=session,
        user_id=user_id,
        user_update=user_patch,
    )
    if updated_user is None:
        raise user_not_found_exp
    return updated_user


@router.delete("/{user_id}", response_model=UserS)
async def delete_user(
    session: SessionDep,
    user_id: int,
) -> Any:
    deleted_user = await UserRepository.delete(session=session, user_id=user_id)
    if deleted_user is None:
        raise user_not_found_exp
    return deleted_user
