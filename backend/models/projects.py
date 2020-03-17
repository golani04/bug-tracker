from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Dict, List, Optional

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
    # FK, that collect all items that is connected to project
    tags: List[str] = field(default_factory=list, repr=False, init=False, compare=False)
    users: List[str] = field(default_factory=list, repr=False, init=False, compare=False)
    issues: List[str] = field(default_factory=list, repr=False, init=False, compare=False)

    def __post_init__(self):
        validate.item_id(self.id)
        validate.item_id(self.maintainer)
        # convert unallowed signs to html codes
        self.name = escape(self.name)
        self.description = escape(self.description)

    @classmethod
    def create(
        cls, name: str, maintainer: str, description: str = "", favorite: bool = False
    ) -> "Project":
        return cls(util.create_id(), name, maintainer, description, favorite)

    @classmethod
    def get_all_projects(cls):
        return [cls(**project) for project in db.get_projects()]

    @classmethod
    def find_by_id(cls, id_: str) -> Optional["Project"]:
        project = [project for project in cls.get_all_projects() if project.id == id_]
        try:
            return project.pop()
        except IndexError:
            return None

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

    def save(self) -> bool:
        projects = self.get_all_projects()
        # add new project to db
        projects.append(self)

        return db.save_projects([project.to_dict() for project in projects])

    def to_dict(self):
        return self._convert_to_custom_dict(self)
