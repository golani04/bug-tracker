from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
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

    owner = relationship("User", back_populates="projects")
