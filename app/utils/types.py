from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_manager import db_manager

SessionDep = Annotated[
    AsyncSession,
    Depends(db_manager.session_getter),
]
