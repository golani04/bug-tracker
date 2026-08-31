from typing import Annotated
from urllib.parse import urljoin

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.repositories.projects import ProjectRepository
from backend.repositories.users import UserRepository
from backend.schemas.users import User as UserSchema, UserUpdate
from backend.services.users import UserService
from backend.utils.auth import auth_manager


router = APIRouter()
me_router = APIRouter()


@me_router.get("/me", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_me(current_user: UserSchema = Depends(auth_manager.get_current_user)):
    return current_user


@router.post("/{user_id}")
async def update_user(
    request: Request,
    user_id: int,
    data: Annotated[UserUpdate, Form()],
    session: Session = Depends(get_db),
):
    service = UserService(UserRepository(session), ProjectRepository(session))
    try:
        service.update(user_id, data)
    except ValueError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Update failed.") from error

    return RedirectResponse(urljoin(str(request.base_url), "user"), status_code=status.HTTP_303_SEE_OTHER)
