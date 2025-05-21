from pydantic import BaseModel, EmailStr

from app.utils.constants import AUTHENTICATION_SCHEME_TYPE
from app.utils.types import AuthenticationSchemeType, TokenType


class TokenResponseS(BaseModel):
    access_token: str
    refresh_token: str | None = None
    authentication_scheme: AuthenticationSchemeType = AUTHENTICATION_SCHEME_TYPE


class TokenPayloadS(BaseModel):
    # required keys
    type: TokenType
    sub: str
    iat: int
    exp: int
    # for access token
    id: int | None = None
    username: str | None = None
    email: EmailStr | None = None
