from fastapi import APIRouter
from backend.api.issues import router as issue_router
from backend.api.users import router as user_router
from backend.api.projects import router as project_router


api_router = APIRouter()

api_router.include_router(issue_router, tags=["Issues"], prefix="/issues")
api_router.include_router(user_router, tags=["Users"], prefix="/users")
api_router.include_router(project_router, tags=["Projects"], prefix="/projects")
