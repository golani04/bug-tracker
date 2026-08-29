from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.repositories.projects import ProjectRepository
from backend.repositories.users import UserRepository
from backend.schemas.users import LoginUser
from backend.services.users import UserService
from backend.utils import error_messages
from backend.utils.auth import auth_manager
from backend.utils.html import templates


router = APIRouter()


@router.get("/logout")
def logout(request: Request):
    response = RedirectResponse("/auth/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.delete_cookie(auth_manager.cookie_name)
    return response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_api(response: Response):
    response.delete_cookie(auth_manager.cookie_name)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "auth/login.html")


@router.post("/login", response_class=JSONResponse, status_code=status.HTTP_200_OK)
async def login(user: LoginUser, session: Session = Depends(get_db)):
    service = UserService(UserRepository(session), ProjectRepository(session))
    try:
        current_user = service.login(user.email, user.password.get_secret_value())
    except ValueError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=error_messages.user_not_found) from error

    response = JSONResponse({"success": True})
    response.set_cookie(
        auth_manager.cookie_name, auth_manager.create_access_token({"id": current_user.id})
    )

    return response
