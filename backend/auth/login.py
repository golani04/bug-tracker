import logging

import pydantic
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.users import User
from backend.schemas.users import UserType


router = APIRouter()
logger = logging.getLogger("bug_tracker")

LoggedInUser = pydantic.dataclasses.dataclass(LoggedInUser)
router = APIRouter()

class LoggedInUser(BaseModel):
    username: str
    password: str

@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
def login(user: LoggedInUser = Body(...), session: Session = Depends(get_db)):
    user = (
        session.query(User)
        .filter(or_(User.email == user.username, User.username == user.username))
        .one_or_none()
    )

    if user is None:
        raise HTTPException(404, detail="User is missing")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
