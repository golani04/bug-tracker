from fastapi import APIRouter

from backend.auth.login import router as login_router


auth_router = APIRouter()

auth_router.include_router(login_router)
