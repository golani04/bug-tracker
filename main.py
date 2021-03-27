import os

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.api import routers
from backend.auth import auth_routers
from backend.general import main_router
from logger import init_logger


app = FastAPI(title="Bug Tracker")
# create logger
init_logger(os.path.abspath(os.path.join(os.path.curdir, "logs", "bug_tracker.log")))


# define routers
app.include_router(routers, prefix="/api/v1")
app.include_router(auth_routers, prefix="/auth")
app.include_router(main_router)


@app.exception_handler(RequestValidationError)
async def validation_exception(request: Request, exc: RequestValidationError) -> JSONResponse:
    return await JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
