from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from backend.api import routers
from backend.auth import auth_routers
from backend.general import main_router
from backend.utils.exceptions import AuthError
from logger import init_logger


app = FastAPI(title="Bug Tracker")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.exception_handler(AuthError)
async def auth_error_handler(request: Request, exc: AuthError) -> RedirectResponse:
    return RedirectResponse("/auth/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


# create logger
init_logger()

# define routers
app.include_router(routers, prefix="/api/v1")
app.include_router(auth_routers, prefix="/auth")
app.include_router(main_router)
