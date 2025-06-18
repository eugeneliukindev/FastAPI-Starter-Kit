from fastapi import APIRouter

from src.api.v1.endpoints.users import router as user_router

api_v1_router = APIRouter(prefix="/v1")

router_list = [
    user_router,
]

for r in router_list:
    api_v1_router.include_router(r)
