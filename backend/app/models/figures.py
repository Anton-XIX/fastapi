from sqlalchemy import JSON, Boolean, Column, Enum, ForeignKey, PickleType, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.mutable import MutableList

from app.core.mixins import DateTimeModelMixinMixin, IdModelMixinMixin
from app.db.base_class import Base
from app.models.choices import FigureType


class FigureBase(Base, IdModelMixinMixin, DateTimeModelMixinMixin):
    __abstract__ = True
    name = Column(String(256), nullable=False)
    figure_type = Column(Enum(FigureType))
    public = Column(Boolean, default=False)
    description = Column(String(256), nullable=True)

    @declared_attr
    def user_uuid(cls):
        return Column(UUID(as_uuid=True), ForeignKey("user.uuid"))


class MultiLineFigure(FigureBase):
    x_axis = Column(MutableList.as_mutable(PickleType))
    datasets = Column(JSON)
