from fastapi import APIRouter
from backend.api.issues import router as issue_router
from backend.api.users import router as user_router


routers = APIRouter()

routers.include_router(issue_router, tags=["Issues"], prefix="/issues")
routers.include_router(user_router, tags=["Users"], prefix="/users")
