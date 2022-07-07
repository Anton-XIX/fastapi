from sqlalchemy import Boolean, Column, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.mixins import DateTimeModelMixinMixin, IdModelMixinMixin
from app.db.base_class import Base
from app.models.choices import TokenType


class Token(Base, IdModelMixinMixin, DateTimeModelMixinMixin):
    token = Column(String(512), nullable=False)
    token_type = Column(Enum(TokenType), nullable=False)
    user_uuid = Column(UUID(as_uuid=True), nullable=False)
    fresh = Column(Boolean, default=True)
    expiration_date = Column(DateTime, nullable=False)
