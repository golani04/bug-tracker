from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.repositories.projects import ProjectRepository
from backend.repositories.users import UserRepository
from backend.schemas.users import UserCreate
from backend.services.users import UserService
from backend.utils.auth import auth_manager
from backend.utils.html import templates


router = APIRouter()


@router.get("/signup", response_class=HTMLResponse)
def sign_up_page(request: Request):
    return templates.TemplateResponse(request, "auth/signup.html")


@router.post("/signup", response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(data: UserCreate, session: Session = Depends(get_db)):
    service = UserService(UserRepository(session), ProjectRepository(session))
    user = service.sign_up(data)

    response = JSONResponse({"success": True}, status_code=status.HTTP_201_CREATED)
    response.set_cookie(auth_manager.cookie_name, auth_manager.create_access_token({"id": user.id}))

    return response
