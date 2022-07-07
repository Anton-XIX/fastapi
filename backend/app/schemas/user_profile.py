import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import UUID4

from app.models.user import UserProfile


class UserProfileCreate(CamelModel):
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[datetime.date]
    user_uuid: UUID4


class UserProfileRegister(CamelModel):
    first_name: Optional[str]
    last_name: Optional[str]


class UserProfileUpdate(CamelModel):
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[datetime.date]

    # @validator("birth_date", pre=True,)
    # def parse_birth_date(cls, value):
    #     return datetime.datetime.strptime(
    #         value,
    #         "%m/%d/%Y"
    #     ).date()

    class Config:
        orm_mode = True
        orig_model = UserProfile


class UserProfileInfo(UserProfileRegister):
    birth_date: Optional[datetime.date]

    class Config:
        orm_mode = True
