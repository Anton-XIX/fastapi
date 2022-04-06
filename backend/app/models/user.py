from sqlalchemy import Boolean, Column, String

from app.core.mixins import DateTimeModelMixinMixin, UuidModelMixinMixin
from app.db.base_class import Base


class User(Base, UuidModelMixinMixin, DateTimeModelMixinMixin):
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False, unique=True)
    is_superuser = Column(Boolean, default=False)
    password = Column(String(256), nullable=False)
    salt = Column(String(256), nullable=False)
