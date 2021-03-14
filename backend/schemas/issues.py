from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from backend.schemas.comment import Comment


Severity = Enum("Severity", "low medium high")
Status = Enum("Status", "opened development review completed")
Label = Enum("Label", "bug enhancement duplicate wontfix")


class IssueBase(BaseModel):
    reporter: UUID
    project: UUID
    title: str
    description: str = ""
    due: Optional[datetime] = None
    severity: Severity = Field(
        Severity.low, description=f"Severity levels: {', '.join(s.name for s in Severity)}."
    )
    status: Status = Field(
        Status.opened, description=f"Statuses: {', '.join(s.name for s in Status)}"
    )
    label: Label = Field(Label.bug, description=f"Issue types: {', '.join(l.name for l in Label)}.")


class IssueCreate(IssueBase):
    pass


class Issue(IssueBase):
    id: int
    updated_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    assignees: List["User"] = []
    comments: List[Comment] = []


from backend.schemas.users import User

Issue.update_forward_refs()
