from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None
    is_superuser: bool = False


class UserPasswordUpdate(BaseModel):
    """
    Users can change their password
    """

    password: constr(min_length=7, max_length=100)
    salt: str


# Properties to receive via API on creation
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


# Additional properties to return via API
class User(UserInDBBase):
    pass
