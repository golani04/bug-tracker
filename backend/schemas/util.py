import secrets
from datetime import timedelta
from typing import Dict, List, Union
from uuid import UUID

from passlib.hash import bcrypt


def create_id():
    return secrets.token_hex()


def find_item_by_id(items: List[Dict], item_id: Union[UUID, int]):
    if isinstance(item_id, UUID):
        item_id = str(item_id)

    return next((item for item in items if item["id"] == item_id), None)


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
