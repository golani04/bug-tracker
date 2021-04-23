from datetime import datetime
from enum import IntEnum
from typing import List, Optional

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


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    updated_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
