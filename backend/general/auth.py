from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.repositories.projects import ProjectRepository
from backend.repositories.users import UserRepository
from backend.schemas.users import LoginUser, UserCreate
from backend.services.users import UserService
from backend.utils.auth import auth_manager
from backend.utils.html import templates


router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "auth/login.html")


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    data: Annotated[LoginUser, Form()],
    session: Session = Depends(get_db),
):
    service = UserService(UserRepository(session), ProjectRepository(session))
    try:
        user = service.login(data.email, data.password.get_secret_value())
    except ValueError as error:
        return templates.TemplateResponse(
            request, "auth/login.html", {"error": str(error)}, status_code=status.HTTP_400_BAD_REQUEST
        )

    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(auth_manager.cookie_name, auth_manager.create_access_token({"id": user.id}))

    return response


@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse(request, "auth/signup.html")


@router.post("/signup", response_class=HTMLResponse)
async def sign_up(
    request: Request,
    data: Annotated[UserCreate, Form()],
    session: Session = Depends(get_db),
):
    service = UserService(UserRepository(session), ProjectRepository(session))
    try:
        user = service.sign_up(data)
    except ValueError as error:
        return templates.TemplateResponse(
            request, "auth/signup.html", {"error": str(error)}, status_code=status.HTTP_409_CONFLICT
        )

    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(auth_manager.cookie_name, auth_manager.create_access_token({"id": user.id}))

    return response


@router.post("/logout")
def logout(request: Request):
    response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(auth_manager.cookie_name)
    return response
