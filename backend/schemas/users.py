from datetime import datetime
from enum import IntEnum
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field  # pylint: disable=no-name-in-module


class UserType(IntEnum):
    admin = 0
    developer = 4
    viewer = 8


class UserBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    role: UserType = Field(UserType.viewer)


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)

    issues: List["Issue"] = Field(default_factory=list)
    projects: List["Project"] = Field(default_factory=list)


# due to circular imports
from backend.schemas.issues import Issue  # noqa: E402
from backend.schemas.projects import Project  # noqa: E402


User.update_forward_refs()
