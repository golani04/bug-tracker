from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str
    maintainer: UUID
    description: str = Field(None)
    favorite: bool = Field(default=False, description="Pproject preference")


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: UUID
    updated_at: datetime = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    users: List["User"] = []
    issues: List["Issue"] = []


# due to circular imports
from backend.models.issues import Issue  # noqa: E402
from backend.models.users import User  # noqa: E402

Project.update_forward_refs()
