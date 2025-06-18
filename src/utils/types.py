from enum import StrEnum
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_manager import db_manager

SessionDep = Annotated[
    AsyncSession,
    Depends(db_manager.session_getter),
]


class LogLevelEnum(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
