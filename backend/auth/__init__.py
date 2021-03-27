from fastapi import APIRouter

from backend.auth.login import router


auth_routers = APIRouter()

auth_routers.include_router(router, tags=["Auth"])
