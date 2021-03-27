from fastapi import APIRouter
from backend.general.routes import router


main_router = APIRouter()

main_router.include_router(router, tags=["Static"])
