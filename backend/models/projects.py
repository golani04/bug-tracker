from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.db import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    active = Column(Boolean, default=True)

    owner = relationship("User", backref="projects")
    issues = relationship("Issue", back_populates="project")

    @classmethod
    def create(cls, name: str, user_id: int):
        return cls(name=name, creator_id=user_id)
