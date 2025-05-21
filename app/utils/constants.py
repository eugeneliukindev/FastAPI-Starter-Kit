from pathlib import Path
from typing import Final

from app.utils.types import AlgorithmType, AuthenticationSchemeType, TokenType

ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent
ALGORITHM: Final[AlgorithmType] = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = 15
REFRESH_TOKEN_EXPIRE_DAYS: Final[int] = 30
ACCESS_TOKEN_TYPE: Final[TokenType] = "access"
REFRESH_TOKEN_TYPE: Final[TokenType] = "refresh"
AUTHENTICATION_SCHEME_TYPE: Final[AuthenticationSchemeType] = "Bearer"
