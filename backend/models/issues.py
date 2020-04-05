from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from enum import Enum
from functools import lru_cache
from typing import ClassVar, Dict, List, Set

from flask import escape
from backend import database as db
from backend.models import util, validate


Severity = Enum("Severity", "low medium high")
Status = Enum("Status", "open done review close")
Label = Enum("Label", "bug enhancement duplicate wontfix")


@dataclass
class Issue:
    id: str
    title: str = field(compare=False, metadata="Describe an issue in short.")
    reporter: str = field(compare=False)  # FK
    assignee: str = field(compare=False)  # FK
    project: str = field(compare=False)  # FK
    severity: Enum = field(default=Severity.low, metadata="Choose severity of the issue.")
    status: Enum = field(default=Status.open, metadata="Choose the progress of the issue.")
    label: Enum = field(default=Label.bug, metadata="Give a disctiption to the issue.")
    description: str = field(
        default="", compare=False, repr=False, metadata="Explain the bug with examples.",
    )
    created: date = field(default_factory=date.today, repr=False)
    due: date = field(default=None, repr=False)
    time_spent: int = field(default=0, repr=False)
    comments: List[str] = field(default_factory=list, repr=False)
    links: List[str] = field(default_factory=list, repr=False)
    # TODO: images: List[str] = field(default_factory=list)
    # define class variable
    unchangeable_props: ClassVar[Set] = {"id", "created", "project", "reporter"}

    def __post_init__(self):
        validate.item_id(self.id)
        validate.item_id(self.assignee)
        validate.item_id(self.reporter)
        validate.item_id(self.project)
        # validate that received value is exist in the enum
        validate.is_enum_has_prop(Severity, self.severity)
        validate.is_enum_has_prop(Status, self.status)
        validate.is_enum_has_prop(Label, self.label)
        validate.is_numeric(self.time_spent)
        validate.is_date(self.created)
        self.due and validate.is_date(self.due)  # allowed to be None
        # convert unallowed signs to html codes
        self.title = escape(self.title)
        self.description = escape(self.description)
        # transform db values to enum
        self.severity = util.value_to_enum(Severity, self.severity)
        self.status = util.value_to_enum(Status, self.status)
        self.label = util.value_to_enum(Label, self.label)
        # timedelta seconds to timedelta
        self.time_spent = timedelta(seconds=(self.time_spent or 0))
        # convert str to dates
        self.created = (
            self.created if isinstance(self.created, date) else date.fromisoformat(self.created)
        )
        self.due = (
            self.due
            if isinstance(self.created, date)
            else (self.due and date.fromisoformat(self.due))
        )  # allowed to be None

    @classmethod
    @lru_cache(1)
    def get_all(cls) -> List["Issue"]:
        return {issue["id"]: cls(**issue) for issue in db.get_issues()}

    @staticmethod
    def _convert_to_custom_dict(issue: "Issue") -> Dict:
        """Convert dataclass to json serializable dict.
           Exclude fields that should not be stored, and convert the
           complex types to the type that can be JSON serializable.
        """

        def serialize_values(val):
            _stringify_this_types = (date,)
            if isinstance(val, _stringify_this_types):
                return str(val)
            if isinstance(val, Enum):
                return val.value
            if isinstance(val, timedelta):
                return util.seconds_to_wdhms(val)

            return val

        return {k: serialize_values(v) for k, v in asdict(issue).items()}

    def to_dict(self) -> Dict:
        return self._convert_to_custom_dict(self)

    @classmethod
    def create(cls, new_issue: Dict) -> "Issue":
        new_issue = {**new_issue, "id": util.create_id(), "created": date.today()}
        return cls(**new_issue)

    def delete(self):
        pass

    def modify(self):
        pass

    def save(self, state: str):
        issues = self.get_all()
        if state in {"create", "modify"}:
            issues[self.id] = self

        # clear cache
        self.get_all.cache_clear()

        return db.save_issues([issue.to_dict() for issue in issues.values()])
