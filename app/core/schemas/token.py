from pydantic import BaseModel

from app.utils.constants import AUTHENTICATION_SCHEME_TYPE
from app.utils.types import AuthenticationSchemeType, TokenType


class TokenResponseS(BaseModel):
    access_token: str
    refresh_token: str | None = None
    authentication_scheme: AuthenticationSchemeType = AUTHENTICATION_SCHEME_TYPE


class TokenPayloadS(BaseModel):
    type: TokenType
    sub: str
    iat: int
    exp: int
    id: int | None = None
    username: str | None = None
    email: str | None = None
