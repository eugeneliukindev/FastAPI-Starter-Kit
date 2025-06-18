import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from main import app as fastapi_app


@pytest_asyncio.fixture(scope="function")
async def aclient():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac
