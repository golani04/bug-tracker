from dataclasses import asdict, dataclass, field, replace
from datetime import date
from enum import Enum
from functools import lru_cache
from typing import ClassVar, Dict, Set, Union

from flask import escape
from backend import database as db
from backend.models import util, validate
from backend.models.base import Base

UserType = Enum("UserType", ["reporter", "qa", "developer", "manager", "admin"])


@dataclass
class User(Base):
    id: str
    name: str
    username: str
    email: str
    password: str
    project: str
    created_at: str = field(default_factory=date.today)
    type: Enum = field(default=UserType.reporter)
    unchangeable_props: ClassVar[Set] = {"id", "created_at", "project"}

    def __post_init__(self):
        validate.item_id(self.id)
        validate.item_id(self.project)
        validate.email(self.email)
        validate.is_enum_has_prop(UserType, self.type)
        validate.is_date(self.created_at)
        # normalize html codes
        self.name = escape(self.name)
        self.username = escape(self.username)
        self.type = util.value_to_enum(UserType, self.type)
        self.created_at = util.set_date(self.created_at)

    @classmethod
    @lru_cache(1)
    def get_all(cls) -> Dict[str, "User"]:
        return {user["id"]: cls(**user) for user in db.get_users()}

    @classmethod
    def create(cls, user: Dict) -> "User":
        # check if password is too short
        password = user.pop("password")
        validate.password(password)
        return cls(
            **{
                **user,
                "id": util.create_id(),
                "created_at": date.today(),
                "password": util.hash_password(password),
            }
        )

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

    def modify(self, data: Dict[str, Union[str, UserType]]) -> "User":
        filtered_data = {k: v for k, v in data.items() if k not in self.unchangeable_props}
        if "password" in filtered_data:
            validate.password(filtered_data["password"])
            filtered_data["password"] = util.hash_password(filtered_data["password"])
        return replace(self, **filtered_data)

    def save(self, state: str = None) -> bool:
        users = self.get_all()
        if state in {"create", "modify"}:
            users[self.id] = self

        # clear cache
        self.get_all.cache_clear()

        return db.save_users([user.to_dict() for user in users.values()])
