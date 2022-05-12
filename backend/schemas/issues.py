from datetime import date, datetime
from enum import IntEnum, auto
from typing import Optional

from pydantic import BaseModel, Field, validator


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
    on_hold = auto()
    in_review = auto()
    completed = auto()
    closed = auto()


class Label(Helpers):
    bug = 1
    enhancement = auto()
    duplicated = auto()
    wontfix = auto()


class IssueBase(BaseModel):
    title: str
    description: str = ""
    reporter: int
    type: Optional[str] = Field(None)
    due: Optional[date] = Field(None)
    severity: Severity = Field(Severity.low, description=f"Severity levels: {Severity.names()}.")
    status: Status = Field(Status.opened, description=f"Statuses: {Status.names()}.")
    label: Label = Field(Label.bug, description=f"Issue types: {Label.names()}.")

    @validator("due", pre=True)
    def parse_due(cls, value: Optional[date]):
        """If value is falsy return null"""

        return value or None


class IssueCreate(IssueBase):
    pass


class IssueUpdate(IssueBase):
    pass


class Issue(IssueBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
