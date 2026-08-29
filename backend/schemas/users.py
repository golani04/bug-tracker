from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: SecretStr


class UserUpdate(BaseModel):
    email: EmailStr | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class LoginUser(BaseModel):
    email: EmailStr
    password: SecretStr
