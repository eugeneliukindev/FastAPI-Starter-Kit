from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import uvicorn
from api import router as api_router
from config import settings
from core.db_manager import db_manager
from fastapi import FastAPI

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
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
