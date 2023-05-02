from enum import IntEnum, auto
from typing import List
from uuid import UUID

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from backend.schemas.users import User


class License(IntEnum):
    free = 1
    trial = auto()
    basic = auto()
    professional = auto()


class OrganizationBase(BaseModel):
    name: str


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: UUID
    license: License

    users: List[User]
