from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.password import verify_password
from app.auth.token import decode_token
from app.core.db_manager import SessionDep
from app.core.schemas.user import UserReadS
from app.exceptions.auth import (
    incorrect_username_or_password_exp,
    invalid_token_type_exc,
)
from app.repository import UserRepository
from app.utils.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.utils.types import TokenType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


async def authenticate_user(session: AsyncSession, username: str, password: str) -> UserReadS:
    user = await UserRepository.get_by_filters(session=session, username=username)
    if user is None or not verify_password(password, user.hashed_password):
        raise incorrect_username_or_password_exp
    return UserReadS.model_validate(user)


def get_token_from_header(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token


async def get_user_from_token(
    session: AsyncSession,
    token: str,
    expected_token_type: TokenType,
) -> UserReadS:
    payload = decode_token(token=token, expected_token_type=expected_token_type)
    username = payload.sub
    user = await UserRepository.get_by_filters(session=session, username=username)
    if user is None:
        raise invalid_token_type_exc
    return UserReadS.model_validate(user)


async def get_user_from_access_token(
    session: SessionDep, token: Annotated[str, Depends(get_token_from_header)]
) -> UserReadS:
    return await get_user_from_token(session=session, token=token, expected_token_type=ACCESS_TOKEN_TYPE)


async def get_user_from_refresh_token(
    session: SessionDep,
    token: Annotated[str, Depends(get_token_from_header)],
) -> UserReadS:
    return await get_user_from_token(session=session, token=token, expected_token_type=REFRESH_TOKEN_TYPE)
