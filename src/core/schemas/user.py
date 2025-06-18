from pydantic import BaseModel, EmailStr


class UserBaseOptionalS(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserBaseS(UserBaseOptionalS):
    username: str
    email: EmailStr


class UserS(UserBaseS):
    id: int


class UserCreateS(UserBaseS):
    pass


class UserPutS(UserBaseS):
    pass


class UserPatchS(UserBaseOptionalS):
    pass
