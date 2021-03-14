import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.utils.auth import hash_password, verify_password
from backend.db import get_db
from backend.models.users import User
from backend.schemas.users import UserType


router = APIRouter()
logger = logging.getLogger("bug_tracker")


class LoggedInUser(BaseModel):
    username: str
    password: str


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoggedInUser, session: Session = Depends(get_db)):
    current_user: User = (
        session.query(User)
        .filter(or_(User.email == user.username, User.username == user.username))
        .one_or_none()
    )

    if current_user is None and not verify_password(user.password, hash_password("timingattack")):
        logger.info(f"{user.username} is missing.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect."
        )

    if not verify_password(user.password, current_user.password):
        logger.info(f"{user.username} entered wrong password.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect."
        )

    return {
        "success": True,
        "is_logged_in": True,
        "username": current_user.username,
        "role": UserType(current_user.role).name,
    }
