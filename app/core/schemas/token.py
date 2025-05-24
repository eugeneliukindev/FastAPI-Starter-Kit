from pydantic import BaseModel, ConfigDict

from app.utils.constants import AUTHENTICATION_SCHEME_TYPE
from app.utils.types import AuthenticationSchemeType, TokenType


class TokenReadS(BaseModel):
    access_token: str
    refresh_token: str | None = None
    authentication_scheme: AuthenticationSchemeType = AUTHENTICATION_SCHEME_TYPE


class TokenPayloadS(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    type: TokenType
    sub: str  # id
    iat: int
    exp: int
    jti: str
