from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel

from backend.schemas.projects import Project


class License(Enum):
    free = 1
    trial = 2
    basic = 3
    professional = 4


class OrganizationBase(BaseModel):
    name: str


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: UUID
    license: License

    projects: List[Project]
