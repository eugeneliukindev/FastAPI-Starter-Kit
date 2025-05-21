from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pydantic_core import ValidationError

from app.config import settings
from app.core.schemas import UserS
from app.core.schemas.token import TokenPayloadS
from app.exceptions.auth import (
    invalid_token_type_exc,
    token_expired_exc,
    unverified_credentials_exc,
)
from app.utils.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_TOKEN_TYPE,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    REFRESH_TOKEN_TYPE,
)
from app.utils.types import TokenType


def encode_token(
    payload: TokenPayloadS,
    key: Any = settings.jwt.private_key.read_text(),
    algorithm: str | None = ALGORITHM,
) -> str:
    try:
        token = jwt.encode(payload=payload.model_dump(), key=key, algorithm=algorithm)
    except jwt.PyJWTError as e:
        raise unverified_credentials_exc from e
    return token


def decode_token(
    token: str,
    key: Any = settings.jwt.public_key.read_text(),
    algorithm: str = ALGORITHM,
) -> TokenPayloadS:
    try:
        payload_dict = jwt.decode(jwt=token, key=key, algorithms=[algorithm])
        payload = TokenPayloadS(**payload_dict)
    except (jwt.InvalidTokenError, ValidationError) as e:
        raise unverified_credentials_exc from e
    return payload


def validate_token(
    payload: TokenPayloadS,
    expected_token_type: TokenType,
) -> None:
    if payload.type != expected_token_type:
        raise invalid_token_type_exc

    timestamp_now = int(datetime.now(UTC).timestamp())

    if timestamp_now > payload.exp:
        raise token_expired_exc
    if timestamp_now < payload.iat:
        raise token_expired_exc


def create_token(
    type_: TokenType,
    user: UserS,
    expires_delta: timedelta,
) -> str:
    now = int(datetime.now(UTC).timestamp())
    exp = now + int(expires_delta.total_seconds())
    sub = user.username
    if type_ == ACCESS_TOKEN_TYPE:
        payload = TokenPayloadS(
            type=ACCESS_TOKEN_TYPE,
            sub=sub,
            iat=now,
            exp=exp,
            id=user.id,
            username=user.username,
            email=user.email,
        )
    else:
        payload = TokenPayloadS(
            type=REFRESH_TOKEN_TYPE,
            sub=sub,
            iat=now,
            exp=exp,
        )
    return encode_token(payload=payload)


def create_access_token(
    user: UserS,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    return create_token(
        type_=ACCESS_TOKEN_TYPE,
        user=user,
        expires_delta=expires_delta,
    )


def create_refresh_token(
    user: UserS, expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
) -> str:
    return create_token(
        type_=REFRESH_TOKEN_TYPE,
        user=user,
        expires_delta=expires_delta,
    )
