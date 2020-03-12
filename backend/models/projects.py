from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Dict, List, Union

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
    _created: date = field(default_factory=date.today, init=False, repr=False)
    _updated: datetime = field(default_factory=datetime.utcnow, init=False, repr=False)
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
        return db.get_projects()

    @staticmethod
    def _convert_non_primitive_data_types_to_str(project: Union[Dict, dataclass]):
        project = project if isinstance(project, dict) else asdict(project)
        types_to_str = (datetime, date)
        return {
            # convert datetime to str
            k: str(v) if isinstance(v, types_to_str) else v
            for k, v in project.items()
        }

    def save(self) -> bool:
        projects = self.get_all_projects()
        # add new project to db
        projects.append(self._convert_non_primitive_data_types_to_str(self))

        return db.save_projects(projects)
