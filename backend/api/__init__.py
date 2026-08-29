from fastapi import APIRouter

from backend.api.issues import router as issue_router
from backend.api.projects import router as project_router
from backend.api.users import me_router, router as user_router


routers = APIRouter()

routers.include_router(me_router, tags=["Users"])
routers.include_router(issue_router, tags=["Issues"], prefix="/issues")
routers.include_router(project_router, tags=["Projects"], prefix="/projects")
routers.include_router(user_router, tags=["Users"], prefix="/users")
