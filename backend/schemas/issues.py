from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from backend.schemas.comment import Comment
from backend.schemas.users import User


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
        Severity.low,
        description=f"Severity level of the issue: {', '.join(severity.name for severity in Severity)}.",  # noqa E501
    )
    status: Status = Field(
        Status.opened,
        description=f"Current status of the issue: {', '.join(status.name for status in Status)}",
    )
    label: Label = Field(
        Label.bug, description=f"Type of an issue: {', '.join(label.name for label in Label)}."
    )


class IssueCreate(IssueBase):
    pass


class Issue(IssueBase):
    id: int
    updated_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    assignees: List[User] = []
    comments: List[Comment] = []
    # TODO: images, links
