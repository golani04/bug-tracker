import re
import secrets
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import List, Union


_ALPHANUMERIC = re.compile(r"[^A-Za-z0-9]+")


@dataclass
class ValidationError(Exception):
    messages: Union[List[str], str]


def item_id(id_: str) -> bool:
    error_msg = ""
    if not isinstance(id_, str):
        error_msg = "ID should be of type string."
    elif len(id_) != len(secrets.token_hex()):
        error_msg = "Invalid ID length."
    elif re.search(_ALPHANUMERIC, id_):
        error_msg = "Has non-alphnumeric values."

    if error_msg:
        raise ValidationError(error_msg)

    return True


def is_enum_has_prop(enum_obj: Enum, enum_prop: Union[Enum, int]) -> bool:
    error = True
    if isinstance(enum_prop, int):
        error = not any(prop.value == enum_prop for prop in enum_obj)
    elif isinstance(enum_prop, Enum):
        error = enum_prop not in enum_obj

    if error:
        raise ValidationError("This {} is missing {}".format(enum_obj, enum_prop))

    return True


def is_numeric(value: Union[int, float]) -> bool:
    if isinstance(value, (int, float)):
        return True

    raise ValidationError(f"Provided value is not numeric: {type(value)}")


def _is_date_types(val: Union[str, date, datetime], date_type: Union[date, datetime]):
    try:
        if isinstance(val, date_type):
            return True
        return bool(date_type.fromisoformat(val))  # format: YYYY-MM-DD
    except (TypeError, ValueError):
        raise ValidationError(
            f"Invalid {date_type.__name__}. Correct format: [YYYY-MM-DD]. Given value: {val}"
        )


def is_date(date_: Union[str, date]) -> bool:
    return _is_date_types(date_, date)  # format: YYYY-MM-DD


def is_datetime(datetime_: Union[str, datetime]) -> bool:
    return _is_date_types(datetime_, datetime)
