from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime

from backend.db import Base


class BaseModel(Base):
    """Shared columns between tables."""

    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc), default=None)
    deleted_at = Column(DateTime, default=None)
    active = Column(Boolean, default=True)

    def delete(self):
        """Soft delete"""
        self.active = False
        self.deleted_at = datetime.now(timezone.utc)
