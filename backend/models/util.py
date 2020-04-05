import secrets
from datetime import timedelta
from enum import Enum
from typing import Dict, Union


def create_id():
    return secrets.token_hex()


def value_to_enum(obj: Enum, value: Union[int, Enum]) -> Enum:
    return value if isinstance(value, obj) else obj(value)


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
