from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


UserType = Enum("UserType", ["reporter", "developer", "manager", "admin"])


class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    type: UserType = Field(UserType.reporter)


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)

    issues: List["Issue"] = []
    projects: List["Project"] = []


# due to circular imports
from backend.schemas.issues import Issue  # noqa: E402
from backend.schemas.projects import Project  # noqa: E402

User.update_forward_refs()
