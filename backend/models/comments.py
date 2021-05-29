from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text

from backend.db import Base


class Comment(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(Text, nullable=False)

    commenter_id = Column(
        Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False
    )
    issue_id = Column(
        Integer, ForeignKey("issues.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, default=None)
    active = Column(Boolean, default=True)
