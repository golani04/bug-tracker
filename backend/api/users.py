from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.db import FileDatabase
from backend.schemas.users import User
from backend.schemas.util import find_item_by_id

router = APIRouter()
db = FileDatabase()


@router.get("/", response_model=List[User])
def get_users():
    return db.get_users()


@router.get("/{user_id}", response_model=User)
def get_issue(user_id: UUID):
    print(db.get_users())
    user = find_item_by_id(db.get_users(), user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Required user is missing"
        )

    return user
