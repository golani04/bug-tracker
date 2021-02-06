from dataclasses import dataclass

import pydantic
from fastapi import Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.auth import router
from backend.db import get_db
from backend.models.users import User


@dataclass
class LoggedInUser:
    username: str
    password: str


LoggedInUser = pydantic.dataclasses.dataclass(LoggedInUser)


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
def login(user: LoggedInUser, session: Session = Depends(get_db)):
    user = session.query.filter(
        or_(User.email == user.username, User.username == user.username)
    ).one_or_none()

    if user is None:
        raise HTTPException(404, detail="User is missing")

    return {}
