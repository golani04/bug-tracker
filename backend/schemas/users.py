from datetime import datetime
from enum import IntEnum
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserType(IntEnum):
    admin = 8  # only me
    manager = 6  # like admin only per organization
    developer = 4
    reporter = 2
    viewer = 1


class UserBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    type: UserType = Field(UserType.viewer)


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)

    issues: List["Issue"] = []


# due to circular imports
from backend.schemas.issues import Issue  # noqa: E402

User.update_forward_refs()
