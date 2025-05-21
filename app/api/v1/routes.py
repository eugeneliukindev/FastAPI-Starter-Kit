from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as user_router

api_v1_router = APIRouter(prefix="/v1")

router_list = [
    user_router,
    auth_router,
]

for r in router_list:
    api_v1_router.include_router(r)
