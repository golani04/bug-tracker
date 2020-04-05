import secrets
from enum import Enum
from typing import Union


def create_id():
    return secrets.token_hex()


def value_to_enum(obj: Enum, value: Union[int, Enum]) -> Enum:
    return value if isinstance(value, obj) else obj(value)
