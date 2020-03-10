from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, List, Union

from flask import escape
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
