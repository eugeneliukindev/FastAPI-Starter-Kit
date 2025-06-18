from httpx import AsyncClient


async def test_get_all_users(aclient: AsyncClient):
    response = await aclient.get("/v1/users")
    assert response.status_code == 200
