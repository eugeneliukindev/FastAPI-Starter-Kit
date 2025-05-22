from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm

from app.auth.dependencies import (
    authenticate_user,
    get_user_from_access_token,
    get_user_from_refresh_token,
)
from app.auth.token import (
    create_access_token,
    create_refresh_token,
)
from app.core.db_manager import SessionDep
from app.core.schemas import UserS
from app.core.schemas.token import TokenResponseS
from app.utils.constants import (
    AUTHENTICATION_SCHEME_TYPE,
)

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(http_bearer)])


@router.post(
    "/token",
    response_model=TokenResponseS,
)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Any:
    user = await authenticate_user(session, form_data.username, form_data.password)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "authentication_scheme": AUTHENTICATION_SCHEME_TYPE,
    }


@router.get(
    "/refresh",
    response_model=TokenResponseS,
    response_model_exclude_none=True,
)
async def refresh(
    user: Annotated[UserS, Depends(get_user_from_refresh_token)],
) -> Any:
    access_token = create_access_token(user=user)
    return {
        "access_token": access_token,
        "authentication_scheme": AUTHENTICATION_SCHEME_TYPE,
    }


@router.get("/me", response_model=UserS)
async def get_me(
    user: Annotated[UserS, Depends(get_user_from_access_token)],
) -> Any:
    return user
