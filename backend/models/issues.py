from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend import models
from backend.enums import Priority, Status
from backend.models.base import BaseModel


class Issue(BaseModel):
    __tablename__ = "issues"

    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[Priority] = mapped_column(String(15), default=Priority.low)
    status: Mapped[Status] = mapped_column(String(15), default=Status.open)

    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE")
    )

    reporter: Mapped["models.users.User"] = relationship("User", back_populates="reporter_issues")
    project: Mapped["models.projects.Project"] = relationship("Project", back_populates="issues")
