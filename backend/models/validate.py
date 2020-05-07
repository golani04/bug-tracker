import re
import secrets
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Dict, List, Union


_ALPHANUMERIC = re.compile(r"[^A-Za-z0-9]+")
# https://owasp.org/www-community/OWASP_Validation_Regex_Repository
_NAIVE_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$"
)


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


def is_time_dict(time_obj: Union[Dict[str, int], int, float]) -> bool:
    """
    Arguments:
        time_obj {Union[int, float]} -- numeric property, is taken from the database
        time_obj {Dict[str, int]} -- dict property, is send from the client

    Raises:
        ValidationError: If type differs from numeric or from timedelta

    Returns:
        bool
    """
    if isinstance(time_obj, dict):
        try:
            timedelta(**time_obj)
            return True
        except TypeError:
            raise ValidationError(f"Provided object is not timedelta object: {type(time_obj)}")

    # is_numeric will raise a ValidationError
    if is_numeric(time_obj):
        return True


def email(addr: str) -> bool:
    if re.fullmatch(_NAIVE_EMAIL_REGEX, addr) is not None:
        return True

    raise ValidationError(f"Email is invalid: {addr}")
