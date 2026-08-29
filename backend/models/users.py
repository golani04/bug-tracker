from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend import models
from backend.models.base import BaseModel
from backend.utils.security import hash_password


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    projects: Mapped[list["models.projects.Project"]] = relationship(
        "Project", back_populates="owner"
    )
    reporter_issues: Mapped[list["models.issues.Issue"]] = relationship(
        "Issue", back_populates="reporter"
    )

    @classmethod
    def create_user(cls, email: str, password: str) -> "User":
        return User(email=email, password_hash=hash_password(password))
