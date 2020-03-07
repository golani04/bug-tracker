from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List


@dataclass
class Project:
    id: str
    name: str = field(compare=False)
    maintainer: str = field(compare=False)
    description: str = field(
        default="",
        repr=False,
        metadata="Describe a project purpose and about in short.",
        compare=False,
    )
    favorite: bool = field(default=False, metadata="Give a project preference.")
    _created: date = field(default_factory=date.today, repr=False)
    _updated: datetime = field(default_factory=datetime.utcnow, repr=False)
    # FK, that collect all items that is connected to project
    tags: List[str] = field(default_factory=list, repr=False, init=False, compare=False)
    users: List[str] = field(default_factory=list, repr=False, init=False, compare=False)
    issues: List[str] = field(default_factory=list, repr=False, init=False, compare=False)

    def __post_init__(self):
        print(self)
