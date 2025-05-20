from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import uvicorn
from fastapi import FastAPI

from app.api.v1.routes import api_v1_router
from app.config import settings
from app.core.db_manager import db_manager

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    yield
    # shutdown
    await db_manager.dispose()


app = FastAPI(
    lifespan=lifespan,
)
app.include_router(
    api_v1_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
