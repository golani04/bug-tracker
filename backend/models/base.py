from abc import ABC, abstractmethod
from datetime import date, datetime
from dataclasses import dataclass, replace

from backend.models import util
from typing import Any, Dict, Optional


@dataclass
class Base(ABC):
    @classmethod
    @abstractmethod
    def get_all(cls):
        """This method is to fetch all items from database"""
        pass

    @classmethod
    def create(cls, data: Dict[str, Any]) -> "Base":
        return cls(**data, id=util.create_id(), created_at=date.today())

    @classmethod
    def find_by_id(cls, id_: str) -> Optional["Base"]:
        return cls.get_all().get(id_)

    @staticmethod
    @abstractmethod
    def _convert_to_custom_dict(model: Any) -> Dict:
        """Convert dataclass to json serializable dict.
           Exclude fields that should not be stored, and convert the
           complex types to the type that can be JSON serializable.
        """
        pass

    def to_dict(self) -> Dict:
        return self._convert_to_custom_dict(self)

    def delete(self) -> "Base":
        return self.get_all().pop(self.id)

    def modify(self, data: Dict) -> "Base":
        unchangeable_props = getattr(self, "unchangeable_props", set())
        data = {k: v for k, v in data.items() if k not in unchangeable_props}
        data["updated_at"] = datetime.utcnow()
        # using `replace` will also invoke post init where the validation runs
        return replace(self, **data)
