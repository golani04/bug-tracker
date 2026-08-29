from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.enums import Priority, Status


class IssueBase(BaseModel):
    title: str
    description: str | None = None
    priority: Priority = Field(Priority.low)
    status: Status = Field(Status.open)


class IssueArgs(BaseModel):
    """Use this schema to validate query params"""

    title: str | None = None
    description: str | None = None
    project_id: int | None = None
    priority: Priority | None = None
    status: Status | None = None
    reporter_id: int | None = None


class IssueCreate(IssueBase):
    pass


class IssueUpdate(IssueArgs):
    pass


class Issue(IssueBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    reporter_id: int
    active: bool
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
