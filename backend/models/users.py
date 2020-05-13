from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from functools import lru_cache
from typing import Dict

from flask import escape
from backend import database as db
from . import validate, util

UserType = Enum("UserType", ["reporter", "qa", "developer", "manager", "admin"])


@dataclass
class User:
    id: str
    name: str
    username: str
    email: str
    password: str
    project: str
    created: str = field(default_factory=date.today)
    type: Enum = field(default=UserType.reporter)

    def __post_init__(self):
        validate.item_id(self.id)
        validate.item_id(self.project)
        validate.email(self.email)
        validate.is_enum_has_prop(UserType, self.type)
        # normalize html codes
        self.name = escape(self.name)
        self.username = escape(self.username)
        self.type = util.value_to_enum(UserType, self.type)
        self.created = util.set_date(self.created)

    @classmethod
    @lru_cache(1)
    def get_all(cls) -> Dict[str, "User"]:
        return {user["id"]: cls(**user) for user in db.get_users()}
