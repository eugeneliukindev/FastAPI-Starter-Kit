from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm

from app.auth.dependencies import (
    authenticate_user,
    get_user_from_refresh_token,
)
from app.auth.password import get_password_hash
from app.auth.token import (
    create_access_token,
    create_refresh_token,
)
from app.core.db_manager import SessionDep
from app.core.schemas import UserCreateS
from app.core.schemas.token import TokenReadS
from app.core.schemas.user import UserCreateDbS, UserReadS
from app.exceptions.auth import already_exists_user_exc
from app.repository import UserRepository
from app.utils.constants import (
    AUTHENTICATION_SCHEME_TYPE,
)

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(http_bearer)])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> TokenReadS:
    user = await authenticate_user(session, form_data.username, form_data.password)
    access_token = create_access_token(user_read_s=user)
    refresh_token = create_refresh_token(user_read_s=user)
    return TokenReadS(
        access_token=access_token,
        refresh_token=refresh_token,
        authentication_scheme=AUTHENTICATION_SCHEME_TYPE,
    )


@router.post("/refresh", response_model_exclude_none=True)
async def refresh(
    user: Annotated[UserReadS, Depends(get_user_from_refresh_token)],
) -> TokenReadS:
    access_token = create_access_token(user_read_s=user)
    return TokenReadS(
        access_token=access_token,
        authentication_scheme=AUTHENTICATION_SCHEME_TYPE,
    )


@router.post("/register")
async def register(user_create_s: UserCreateS, session: SessionDep) -> TokenReadS:
    existing_user = await UserRepository.check_already_exists(
        session=session,
        username=user_create_s.username,
        email=str(user_create_s.email),
    )
    if existing_user:
        raise already_exists_user_exc
    hashed_password = get_password_hash(password=user_create_s.password)
    user_create_db_s = UserCreateDbS(
        username=user_create_s.username,
        hashed_password=hashed_password,
        email=user_create_s.email,
    )
    user = await UserRepository.create(session=session, user_create_db_s=user_create_db_s)
    user_read_s = UserReadS.model_validate(user)
    access_token = create_access_token(user_read_s=user_read_s)
    refresh_token = create_refresh_token(user_read_s=user_read_s)
    return TokenReadS(
        access_token=access_token,
        refresh_token=refresh_token,
        authentication_scheme=AUTHENTICATION_SCHEME_TYPE,
    )
