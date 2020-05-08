import secrets
from datetime import date, datetime, timedelta
from enum import Enum
from passlib.hash import bcrypt
from typing import Any, Dict, Optional, Union


def create_id():
    return secrets.token_hex()


def value_to_enum(obj: Enum, value: Union[int, Enum]) -> Enum:
    return value if isinstance(value, obj) else obj(value)


def allow_none(f):
    def wrapper(value: Any, allowed_none: bool = False) -> Optional[Any]:
        if allowed_none and value is None:
            return None
        return f(value)

    return wrapper


def _set_datetimes(
    dates: Union[str, date, datetime], types: Union[date, datetime]
) -> Union[date, datetime]:
    return dates if isinstance(dates, types) else types.fromisoformat(dates)


@allow_none
def set_date(date_: Union[date, datetime]):
    return _set_datetimes(date_, date)


@allow_none
def set_datetime(datetime_: Union[str, datetime]):
    return _set_datetimes(datetime_, datetime)


def seconds_to_wdhms(td: timedelta) -> Dict[str, int]:
    """Convert timedelta object.

        Returns:
            [dict]: {'weeks': 0, 'days': 0, 'hours': 0, 'minutes':0, 'seconds': 0}
    """
    if not isinstance(td, timedelta):
        raise ValueError(
            (
                f"Incorrect type of variable is passed. Provided type: {type(td)} "
                "and should be of timedelta type."
            )
        )
    weeks, days = divmod(td.days, 7)
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return dict(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)


def wdhms_to_seconds(wdmhs: Union[Dict[str, int], int]) -> int:
    """Convert timedelda dict to seconds

        Arguments:
            [dict]: {'weeks': 0, 'days': 0, 'hours': 0, 'minutes':0, 'seconds': 0}
    """
    return wdmhs if isinstance(wdmhs, (int, float)) else timedelta(**wdmhs).total_seconds()


def hash_password(passw: str) -> str:
    return bcrypt.hash(passw)


def verify_password(passw: str, hashed: str) -> bool:
    return bcrypt.verify(passw, hashed)
