from sqlalchemy import Boolean, Column, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship

from app.core.mixins import DateTimeModelMixinMixin, IdModelMixinMixin, UuidModelMixinMixin
from app.db.base_class import Base


class User(Base, UuidModelMixinMixin, DateTimeModelMixinMixin):
    email = Column(String, index=True, nullable=False, unique=True)
    is_superuser = Column(Boolean, default=False)
    password = Column(String(256), nullable=False)
    salt = Column(String(256), nullable=False)
    profile = relationship("UserProfile", uselist=False, backref="user")
    figures = relationship("MultiLineFigure", backref="user", lazy="dynamic")
    # profile = relationship("UserProfile", backref=backref("user", uselist=False))


class UserProfile(Base, IdModelMixinMixin, DateTimeModelMixinMixin):
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    birth_date = Column(Date(), nullable=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), unique=True)
    # user_uuid = Column(UUID(as_uuid=True), ForeignKey('user.uuid', ondelete='CASCADE'))
    # user = relationship("User", back_populates="profile")
