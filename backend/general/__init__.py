from fastapi import APIRouter

from backend.general.auth import router as auth_pages_router
from backend.general.routes import router


main_router = APIRouter()

main_router.include_router(auth_pages_router, tags=["Static"])
main_router.include_router(router, tags=["Static"])
