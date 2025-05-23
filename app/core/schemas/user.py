from datetime import datetime
from typing import final

from pydantic import BaseModel, ConfigDict, EmailStr, PositiveInt


class UserBaseS(BaseModel):
    pass


class UserCreateS(UserBaseS):
    username: str
    password: str
    email: EmailStr


class UserCreateDbS(UserBaseS):
    username: str
    hashed_password: str
    email: EmailStr


@final
class UserS(UserBaseS):  # UserOrm
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    username: str
    email: EmailStr
    hashed_password: str  # !
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None


class UserReadS(UserBaseS):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None


class UserUpdateS(UserBaseS):
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserPutS(UserBaseS):
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserPatchS(UserBaseS):
    username: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None
