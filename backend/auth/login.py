from dataclasses import dataclass

import pydantic
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.users import User


@dataclass
class LoggedInUser:
    username: str
    password: str


LoggedInUser = pydantic.dataclasses.dataclass(LoggedInUser)
router = APIRouter()


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
