from datetime import date, datetime
from enum import IntEnum, auto
from typing import Optional

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


class Helpers(IntEnum):
    def __str__(self):
        return self.name

    @classmethod
    def names(cls):
        return [item.name for item in cls]

    @classmethod
    def values(cls):
        return [item.value for item in cls]


class Severity(Helpers):
    low = 1
    medium = auto()
    high = auto()


class Status(Helpers):
    opened = 1
    in_progress = auto()
    in_review = auto()
    completed = auto()


class Label(Helpers):
    bug = 1
    enhancement = auto()
    duplicate = auto()
    wontfix = auto()


class IssueBase(BaseModel):
    reporter: int
    project_id: int
    title: str
    description: str = ""
    due: Optional[date] = None
    severity: Severity = Field(
        Severity.low, description=f"Severity levels: {', '.join(Severity.names())}."
    )
    status: Status = Field(Status.opened, description=f"Statuses: {', '.join(Status.names())}")
    label: Label = Field(Label.bug, description=f"Issue types: {', '.join(Label.names())}.")


class IssueCreate(IssueBase):
    pass


class Issue(IssueBase):
    id: int
    updated_at: Optional[datetime] = None  # pylint: disable=unsubscriptable-object
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
