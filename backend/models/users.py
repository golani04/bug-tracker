from dataclasses import asdict, dataclass, field, replace
from datetime import date
from enum import Enum
from functools import lru_cache
from typing import ClassVar, Dict, Set, Optional, Union

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
    unchangeable_props: ClassVar[Set] = {"id", "created", "project"}

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

    @classmethod
    def create(cls, user: Dict) -> "User":
        # check if password is short
        password = user.pop("password")
        validate.password(password)
        return cls(
            **{
                **user,
                "id": util.create_id(),
                "created": date.today(),
                "password": util.hash_password(password),
            }
        )

    @classmethod
    def find_by_id(cls, id_: str) -> Optional["User"]:
        return cls.get_all().get(id_)

    @staticmethod
    def _convert_to_custom_dict(user: "User") -> Dict:
        """Convert dataclass to json serializable dict.
           Exclude fields that should not be stored, and convert the
           complex types to the type that can be JSON serializable.
        """

        def convert(v: Union[str, Enum]):
            _stringify = (date,)
            if isinstance(v, _stringify):
                return str(v)
            if isinstance(v, Enum):
                return v.value

            return v

        return {k: convert(v) for k, v in asdict(user).items()}

    def to_dict(self) -> Dict:
        return self._convert_to_custom_dict(self)

    def modify(self, data: Dict[str, Union[str, UserType]]) -> "User":
        filtered_data = {k: v for k, v in data.items() if k not in self.unchangeable_props}
        if "password" in filtered_data:
            validate.password(filtered_data["password"])
            filtered_data["password"] = util.hash_password(filtered_data["password"])
        return replace(self, **filtered_data)

    def delete(self) -> "User":
        return User.get_all().pop(self.id)

    def save(self, state: str = None) -> bool:
        users = self.get_all()
        if state in {"create", "modify"}:
            users[self.id] = self

        # clear cache
        self.get_all.cache_clear()

        return db.save_users([user.to_dict() for user in users.values()])
