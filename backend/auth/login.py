import logging
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import Row, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound

from backend.db import get_db
from backend.models.users import User
from backend.utils import error_messages
from backend.utils.auth import auth_manager
from backend.utils.html import templates
from backend.utils.security import hash_password, verify_password


router = APIRouter()
logger = logging.getLogger("bug_tracker")


@router.get("/logout")
def logout(request: Request):
    response = RedirectResponse("/auth/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.delete_cookie(auth_manager.cookie_name)
    return response


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", context={"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(
    username: str = Form(...), password: str = Form(...), sess: Session = Depends(get_db)
):
    stmt = select(User.id, User.password).where(
        or_(User.email == username, User.username == username)
    )
    try:
        current_user: Row[tuple[int, str]] | None
        if (current_user := sess.execute(stmt).one_or_none()) is None:
            raise ValueError
    except (MultipleResultsFound, ValueError) as e:
        if isinstance(e, MultipleResultsFound):
            logger.error(f"Multiple users are found for this {username=}")

        verify_password("timingattack", hash_password("timingattack"))
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=error_messages.user_not_found) from e

    user_id, user_pwd = current_user
    if not verify_password(password, user_pwd.encode()):
        verify_password("timingattack", hash_password("timingattack"))
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=error_messages.user_not_found)

    response = RedirectResponse("/issues", status.HTTP_303_SEE_OTHER)
    response.set_cookie(auth_manager.cookie_name, auth_manager.create_access_token({"id": user_id}))

    return response
