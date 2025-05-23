import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pydantic_core import ValidationError

from app.config import settings
from app.core.schemas.token import TokenPayloadS
from app.core.schemas.user import UserReadS
from app.exceptions.auth import (
    expired_token_exc,
    invalid_token_type_exc,
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
        token = jwt.encode(payload=payload.model_dump(exclude_none=True), key=key, algorithm=algorithm)
    except jwt.PyJWTError as e:
        raise unverified_credentials_exc from e
    return token


def decode_token(
    token: str,
    expected_token_type: TokenType,
    key: Any = settings.jwt.public_key.read_text(),
    algorithm: str = ALGORITHM,
) -> TokenPayloadS:
    try:
        payload_dict = jwt.decode(
            jwt=token,
            key=key,
            algorithms=[algorithm],
            options=settings.jwt.options,
        )
        payload = TokenPayloadS(**payload_dict)

        if payload.type != expected_token_type:
            raise invalid_token_type_exc

    except jwt.ExpiredSignatureError as e:
        raise expired_token_exc from e
    except jwt.MissingRequiredClaimError as e:
        raise unverified_credentials_exc from e
    except jwt.InvalidTokenError as e:
        raise unverified_credentials_exc from e
    except ValidationError as e:
        raise unverified_credentials_exc from e
    except Exception as e:
        raise unverified_credentials_exc from e

    return payload


def create_token(
    type_: TokenType,
    user_read_s: UserReadS,
    expires_delta: timedelta,
) -> str:
    now = int(datetime.now(UTC).timestamp())
    exp = now + int(expires_delta.total_seconds())
    sub = user_read_s.username
    jti = uuid.uuid4().hex
    if type_ == ACCESS_TOKEN_TYPE:
        payload = TokenPayloadS(
            type=ACCESS_TOKEN_TYPE,
            sub=sub,
            iat=now,
            exp=exp,
            jti=jti,
            id=user_read_s.id,
            username=user_read_s.username,
            email=user_read_s.email,
        )
    else:
        payload = TokenPayloadS(
            type=REFRESH_TOKEN_TYPE,
            sub=sub,
            iat=now,
            exp=exp,
            jti=jti,
        )
    return encode_token(payload=payload)


def create_access_token(
    user_read_s: UserReadS,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    return create_token(
        type_=ACCESS_TOKEN_TYPE,
        user_read_s=user_read_s,
        expires_delta=expires_delta,
    )


def create_refresh_token(
    user_read_s: UserReadS, expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
) -> str:
    return create_token(
        type_=REFRESH_TOKEN_TYPE,
        user_read_s=user_read_s,
        expires_delta=expires_delta,
    )
