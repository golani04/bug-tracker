from dataclasses import asdict, dataclass, field, replace
from datetime import date, datetime
from functools import lru_cache
from typing import ClassVar, Dict, List, Set, Optional

from flask import escape
from backend import database as db
from backend.models import validate, util


@dataclass
class Project:
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
    created: date = field(default_factory=date.today, repr=False)
    updated: datetime = field(default_factory=datetime.utcnow, repr=False)
    # TODO: access - private, public, limited
    # FK, that collect all items that is connected to project
    tags: List[str] = field(default_factory=list, repr=False, init=False, compare=False)
    users: List[str] = field(default_factory=list, repr=False, init=False, compare=False)
    issues: List[str] = field(default_factory=list, repr=False, init=False, compare=False)
    # define class variable
    unchangeable_props: ClassVar[Set] = {"id", "created", "updated"}

    def __post_init__(self):
        validate.item_id(self.id)
        validate.item_id(self.maintainer)
        validate.is_date(self.created)
        validate.is_datetime(self.updated)
        # convert unallowed signs to html codes
        self.name = escape(self.name)
        self.description = escape(self.description)
        # least needed property, don't raise ValidationError, assign default value
        self.favorite = self.favorite if isinstance(self.favorite, bool) else False
        # convert str to date[time] formats
        self.created = (
            self.created if isinstance(self.created, date) else date.fromisoformat(self.created)
        )
        self.updated = (
            self.updated
            if isinstance(self.updated, datetime)
            else datetime.fromisoformat(self.updated)
        )

    @classmethod
    def create(
        cls, name: str, maintainer: str, description: str = "", favorite: bool = False
    ) -> "Project":
        return cls(util.create_id(), name, maintainer, description, favorite)

    @classmethod
    @lru_cache(1)
    def get_all_projects(cls) -> List["Project"]:
        return {project["id"]: cls(**project) for project in db.get_projects()}

    @classmethod
    def find_by_id(cls, id_: str) -> Optional["Project"]:
        return cls.get_all_projects().get(id_)

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

    def to_dict(self) -> Dict:
        return self._convert_to_custom_dict(self)

    def delete(self) -> "Project":
        return self.get_all_projects().pop(self.id)

    def modify(self, data: Dict) -> "Project":
        data = {k: v for k, v in data.items() if k not in self.unchangeable_props}
        data["updated"] = datetime.utcnow()
        return replace(self, **data)

    def save(self, state: str = None) -> bool:
        projects = self.get_all_projects()
        if state in {"create", "modify"}:
            projects[self.id] = self

        # clear cache
        self.get_all_projects.cache_clear()

        return db.save_projects([project.to_dict() for project in projects.values()])
