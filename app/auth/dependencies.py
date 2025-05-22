from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.password import verify_password
from app.auth.token import decode_and_validate_token
from app.core.db_manager import SessionDep
from app.core.schemas import UserS
from app.exceptions.auth import (
    incorrect_username_or_password_exp,
    invalid_token_type_exc,
)
from app.repository import UserRepository
from app.utils.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.utils.types import TokenType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> UserS:
    user = await UserRepository.get_by_username(session=session, username=username)
    if user is None or not verify_password(password, user.hashed_password):
        raise incorrect_username_or_password_exp
    return UserS.model_validate(user, from_attributes=True)


def get_token_from_header(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token


async def get_user_from_token(
    session: AsyncSession,
    token: str,
    expected_token_type: TokenType,
) -> UserS:
    payload = decode_and_validate_token(
        token=token, expected_token_type=expected_token_type
    )
    user = await UserRepository.get_by_username(session=session, username=payload.sub)
    if user is None:
        raise invalid_token_type_exc
    return UserS.model_validate(user, from_attributes=True)


async def get_user_from_access_token(
    session: SessionDep, token: Annotated[str, Depends(get_token_from_header)]
) -> UserS:
    return await get_user_from_token(
        session=session, token=token, expected_token_type=ACCESS_TOKEN_TYPE
    )


async def get_user_from_refresh_token(
    session: SessionDep,
    token: Annotated[str, Depends(get_token_from_header)],
) -> UserS:
    return await get_user_from_token(
        session=session, token=token, expected_token_type=REFRESH_TOKEN_TYPE
    )
