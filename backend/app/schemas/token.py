from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TokenCreate(BaseModel):
    token: str
    token_type: str
    user_uuid: UUID
    fresh: Optional[bool]


class TokenUpdate(TokenCreate):
    ...


class RenewToken(BaseModel):
    refresh_token: Optional[str]
