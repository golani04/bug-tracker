from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.repositories.projects import ProjectRepository
from backend.repositories.users import UserRepository
from backend.schemas.users import LoginUser, User as UserSchema, UserCreate
from backend.services.users import UserService
from backend.utils import error_messages
from backend.utils.auth import auth_manager


router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def sign_up(data: UserCreate, response: Response, session: Session = Depends(get_db)):
    service = UserService(UserRepository(session), ProjectRepository(session))
    try:
        user = service.sign_up(data)
    except ValueError as error:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(error)) from error

    response.set_cookie(auth_manager.cookie_name, auth_manager.create_access_token({"id": user.id}))

    return user


@router.post("/login", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def login(user: LoginUser, response: Response, session: Session = Depends(get_db)):
    service = UserService(UserRepository(session), ProjectRepository(session))
    try:
        current_user = service.login(user.email, user.password.get_secret_value())
    except ValueError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=error_messages.user_not_found) from error

    response.set_cookie(
        auth_manager.cookie_name, auth_manager.create_access_token({"id": current_user.id})
    )

    return current_user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie(auth_manager.cookie_name)
