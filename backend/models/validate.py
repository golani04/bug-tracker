import re
import secrets
from dataclasses import dataclass
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
