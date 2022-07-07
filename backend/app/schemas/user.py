from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import EmailStr, constr

from app.core.utils import to_snake_case
from app.models.user import User
from app.schemas.user_profile import UserProfileInfo, UserProfileRegister


class UserLogin(CamelModel):
    email: EmailStr = None
    password: str = None


class UserBase(CamelModel):
    email: Optional[EmailStr] = None
    is_superuser: bool = False


class UserPasswordUpdate(CamelModel):
    password: constr(min_length=7, max_length=100)
    salt: str


class UserCreate(UserBase):
    email: EmailStr
    password: str
    salt: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserRegister(UserLogin):
    user_profile: UserProfileRegister


class UserInfo(UserBase):
    profile: UserProfileInfo or None = None

    class Config:
        orm_mode = True
        orig_model = User
