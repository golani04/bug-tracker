from datetime import date, datetime
from dataclasses import dataclass, field
from typing import List

from .util import ItemID


@dataclass
class Project:
    id: ItemID
    name: str
    maintainer: ItemID
    description: str = field(default="", metadata="Describe a project purpose and about in short.")
    favorite: bool = field(default=False, metadata="Give a project preference.")
    _created: date = field(default_factory=date.today)
    _updated: datetime = field(default_factory=datetime.utcnow)
    # FK, that collect all items that is connected to project
    tags: List[ItemID] = field(default_factory=list)
    users: List[ItemID] = field(default_factory=list)
    issues: List[ItemID] = field(default_factory=list)
