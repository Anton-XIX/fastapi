import datetime
from typing import Optional
from uuid import UUID

from fastapi_camelcase import CamelModel
from pydantic import BaseModel


class TokenCreate(CamelModel):
    token: str
    token_type: str
    user_uuid: UUID
    expiration_date: datetime.datetime
    fresh: Optional[bool]


class TokenDisable(CamelModel):
    fresh: bool


class TokenUpdate(CamelModel):
    token: Optional[str]
    token_type: Optional[str]
    user_uuid: Optional[UUID]
    expiration_date: Optional[datetime.datetime]
    fresh: Optional[bool]


class RenewToken(CamelModel):
    refresh_token: Optional[str]
