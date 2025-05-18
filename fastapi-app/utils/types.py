from typing import Annotated

from core.db_manager import db_manager
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep = Annotated[
    AsyncSession,
    Depends(db_manager.session_getter),
]
