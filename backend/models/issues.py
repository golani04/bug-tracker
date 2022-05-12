from sqlalchemy import Column, Date, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import relationship

from backend.models.base import BaseModel
from backend.schemas.issues import Label, Severity, Status


class Issue(BaseModel):
    __tablename__ = "issues"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(255), nullable=False)
    type = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    severity = Column(SmallInteger, default=int(Severity.low))
    status = Column(SmallInteger, default=int(Status.opened))
    label = Column(SmallInteger, default=int(Label.bug))
    due = Column(Date, nullable=True)

    reporter = Column(
        Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User", back_populates="issues")
