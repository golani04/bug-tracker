import logging
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.users import User
from backend.schemas.users import UserCreate
from backend.utils.auth import auth_manager
from backend.utils.html import templates


router = APIRouter()
logger = logging.getLogger("bug_tracker")


@router.get("/signup", response_class=HTMLResponse)
def sign_up_page(request: Request):
    return templates.TemplateResponse("auth/signup.html", context={"request": request})


@router.post("/signup", response_class=HTMLResponse)
async def sign_up(request: Request, sess: Session = Depends(get_db)):
    new_user: UserCreate = UserCreate(**await request.form())
    user: User = User.create_user(**new_user.dict())

    sess.add(user)
    sess.commit()
    sess.refresh(user)

    response = RedirectResponse("/issues", status.HTTP_303_SEE_OTHER)
    response.set_cookie(auth_manager.cookie_name, auth_manager.create_access_token({"id": user.id}))

    return response
