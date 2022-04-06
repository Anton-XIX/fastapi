import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID


class DateTimeModelMixinMixin(object):
    created_at = Column(
        DateTime,
        default=datetime.now,
    )
    updated_at = Column(DateTime, onupdate=datetime.now)


class IdModelMixinMixin(object):
    id = Column(Integer, primary_key=True, index=True)


class UuidModelMixinMixin(object):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
