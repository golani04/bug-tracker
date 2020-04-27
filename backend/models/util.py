import secrets
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Dict, Optional, Union


def create_id():
    return secrets.token_hex()


def value_to_enum(obj: Enum, value: Union[int, Enum]) -> Enum:
    return value if isinstance(value, obj) else obj(value)


# TODO: eleminate code repeat for assigning date/dateimes values
def set_date(date_: Optional[Union[str, date]], allowed_none: bool = False):
    if allowed_none and date_ is None:
        return date_

    return date_ if isinstance(date_, date) else date.fromisoformat(date_)


def set_datetime(datetime_: Optional[Union[str, datetime]], allowed_none: bool = False):
    if allowed_none and datetime_ is None:
        return datetime_

    return datetime_ if isinstance(datetime_, datetime) else datetime.fromisoformat(datetime_)


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


def wdhms_to_seconds(wdmhs: Union[Dict[str, int], int]) -> timedelta:
    """[dict]: {'weeks': 0, 'days': 0, 'hours': 0, 'minutes':0, 'seconds': 0}"""
    return wdmhs if isinstance(wdmhs, int) else timedelta(**wdmhs).total_seconds()
