from datetime import datetime

from sqlalchemy import Column, DateTime, Date, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import relationship

from backend.db import Base
from backend.schemas.issues import Label, Severity, Status


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(SmallInteger, default=int(Severity.low))
    status = Column(SmallInteger, default=int(Status.opened))
    label = Column(SmallInteger, default=int(Label.bug))
    due = Column(Date, nullable=True)

    reporter = Column(
        Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False
    )
    project_id = Column(
        Integer, ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    owner = relationship("User", backref="issues")
    project = relationship("Project", back_populates="issues")
