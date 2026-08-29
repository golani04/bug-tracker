from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend import models
from backend.models.base import BaseModel


class Project(BaseModel):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(100))
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")
    )

    owner: Mapped["models.users.User"] = relationship("User", back_populates="projects")
    issues: Mapped[list["models.issues.Issue"]] = relationship("Issue", back_populates="project")
