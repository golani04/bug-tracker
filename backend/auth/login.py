from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.users import User
from backend.utils.auth import auth_manager
from backend.utils.html import templates
from backend.utils.security import verify_password


router = APIRouter()


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
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    current_user: User = (
        db.query(User).filter(or_(User.email == username, User.username == username)).one_or_none()
    )

    if current_user is None:
        verify_password("timingattack", b"timingattack")
        raise HTTPException(404, detail="Username or password are incorrect")

    if not verify_password(password, current_user.password):
        raise HTTPException(404, detail="Username or password are incorrect")

    response = RedirectResponse("/issues", status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        auth_manager.cookie_name, auth_manager.create_access_token({"id": current_user.id})
    )

    return response
