from datetime import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from backend.utils.time import utcnow


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    """Shared columns between tables."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=utcnow, default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    def delete(self):
        """Soft delete"""

        self.active = False
        self.deleted_at = utcnow()
