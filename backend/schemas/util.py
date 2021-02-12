import secrets
from typing import Dict, List, Union
from uuid import UUID


def create_id():
    return secrets.token_hex()


def find_item_by_id(items: List[Dict], item_id: Union[UUID, int]):
    if isinstance(item_id, UUID):
        item_id = str(item_id)

    return next((item for item in items if item["id"] == item_id), None)
