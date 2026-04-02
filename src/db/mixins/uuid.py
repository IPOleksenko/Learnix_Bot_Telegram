import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column

class UUIDMixin:
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)