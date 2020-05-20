from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from functools import lru_cache
from typing import ClassVar, Dict, List, Set, Optional

from flask import escape
from backend import database as db
from backend.models import validate, util
from backend.models.base import Base
from backend.models.issues import Issue


@dataclass
class Project(Base):
    id: str
    name: str = field(compare=False, metadata="Give your project a name.")
    maintainer: str = field(compare=False)
    description: str = field(
        default="",
        repr=False,
        metadata="Describe a project purpose and about in short.",
        compare=False,
    )
    favorite: bool = field(default=False, metadata="Give a project preference.")
    created_at: date = field(default_factory=date.today, repr=False)
    updated_at: datetime = field(default_factory=datetime.utcnow, repr=False)
    # FK, collect all items that is connected to project
    users: List[str] = field(default_factory=list, repr=False, init=False, compare=False)
    issues: Set[str] = field(default_factory=set, repr=False, compare=False)
    # define class variable
    unchangeable_props: ClassVar[Set] = {"id", "created_at", "updated_at"}

    def __post_init__(self):
        validate.item_id(self.id)
        validate.item_id(self.maintainer)
        validate.is_date(self.created_at)
        validate.is_datetime(self.updated_at)
        # convert unallowed signs to html codes
        self.name = escape(self.name)
        self.description = escape(self.description)
        # least needed property, don't raise ValidationError, assign default value
        self.favorite = self.favorite if isinstance(self.favorite, bool) else False
        # convert str to date[time] formats
        self.created_at = util.set_date(self.created_at)
        self.updated_at = util.set_datetime(self.updated_at)

    @staticmethod
    def _convert_to_custom_dict(project: "Project") -> Dict:
        """Convert dataclass to json serializable dict.
           Exclude fields that should not be stored, and convert the
           complex types to the type that can be JSON serializable.
        """
        _json_not_serializable_types = (datetime, date)
        _excluded_fields = {"tags", "issues", "users"}
        return {
            # convert datetime to str
            k: str(v) if isinstance(v, _json_not_serializable_types) else v
            for k, v in asdict(project).items()
            if k not in _excluded_fields
        }

    @classmethod
    @lru_cache(1)
    def get_all(cls) -> List["Project"]:
        return {project["id"]: cls(**project) for project in db.get_projects()}

    def get_issue(self, issue_id: str) -> Optional[Issue]:
        issue = Issue.find_by_id(issue_id)
        if not self.issues:
            return issue if issue is not None and self.id == issue.project else None

        return issue if issue_id in self.issues else None

    def get_issues(self) -> List[Issue]:
        project_issues = []

        if self.issues:
            issues = Issue.get_all()
            project_issues = [issues[id_] for id_ in self.issues if id_ in issues]
        else:
            project_issues = Issue.search({"project": self.id})

        # this if agains solid pronsiples, single responsibility principle
        # TODO: remove when db will be changed from files to SQL
        if not self.issues or len(self.issues) != len(project_issues):
            self.issues = [issue.id for issue in project_issues]
            self.save("modify")

        return project_issues

    def save(self, state: str = None) -> bool:
        projects = self.get_all()
        if state in {"create", "modify"}:
            projects[self.id] = self

        # clear cache
        self.get_all.cache_clear()

        return db.save_projects([project.to_dict() for project in projects.values()])
