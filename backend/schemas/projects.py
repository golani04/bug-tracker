from datetime import datetime
from typing import List, Optional
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
    updated_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    users: List["User"] = []
    issues: List["Issue"] = []


# due to circular imports
from backend.schemas.issues import Issue  # noqa: E402
from backend.schemas.users import User  # noqa: E402

# in order to use refs in type declaration
Project.update_forward_refs()
