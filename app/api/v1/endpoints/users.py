from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any

from fastapi import (
    APIRouter,
    Depends,
)

from app.auth.dependencies import get_user_from_access_token
from app.auth.password import get_password_hash
from app.core.db_manager import SessionDep
from app.core.schemas import UserCreateS, UserPutS
from app.core.schemas.user import UserCreateDbS, UserPatchS, UserReadS
from app.exceptions.users import user_not_found_exp
from app.repository import UserRepository

if TYPE_CHECKING:
    from typing import Any

router = APIRouter(tags=["Users"], prefix="/users")


@router.get("", response_model=list[UserReadS])
async def get_all_users(
    session: SessionDep,
) -> Any:
    users = await UserRepository.get_all(session=session)
    return users


@router.post("", response_model=UserReadS)
async def create_user(
    session: SessionDep,
    user_create: UserCreateS,
) -> Any:
    hashed_password = get_password_hash(password=user_create.password)
    user_create_db_s = UserCreateDbS(
        username=user_create.username,
        hashed_password=hashed_password,
        email=user_create.email,
    )
    user = await UserRepository.create(
        session=session,
        user_create_db_s=user_create_db_s,
    )
    return user


@router.get("/me")
async def get_me(user: Annotated[UserReadS, Depends(get_user_from_access_token)]) -> Any:
    return user


@router.get("/{user_id}", response_model=UserReadS)
async def get_user(
    user_id: int,
    session: SessionDep,
) -> Any:
    user = await UserRepository.get(session=session, user_id=user_id)
    if user is None:
        raise user_not_found_exp
    return user


@router.put("/{user_id}", response_model=UserReadS)
async def update_user_partial(
    session: SessionDep,
    user_id: int,
    user_put: UserPutS,
) -> Any:
    updated_user = await UserRepository.update(session=session, user_id=user_id, user_update=user_put)
    if updated_user is None:
        raise user_not_found_exp
    return updated_user


@router.patch("/{user_id}", response_model=UserReadS)
async def update_user(
    session: SessionDep,
    user_id: int,
    user_patch: UserPatchS,
) -> Any:
    updated_user = await UserRepository.update(session=session, user_id=user_id, user_update=user_patch)
    if updated_user is None:
        raise user_not_found_exp
    return updated_user


@router.delete("/{user_id}", response_model=UserReadS)
async def delete_user(
    session: SessionDep,
    user_id: int,
) -> Any:
    deleted_user = await UserRepository.delete(session=session, user_id=user_id)
    if deleted_user is None:
        raise user_not_found_exp
    return deleted_user
