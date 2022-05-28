from fastapi import APIRouter

from backend.auth.login import router as login_router
from backend.auth.sign_up import router as signup_router


auth_routers = APIRouter(tags=["Auth"])

auth_routers.include_router(login_router)
auth_routers.include_router(signup_router)
