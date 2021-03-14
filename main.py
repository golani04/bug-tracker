import os

from fastapi import FastAPI

from backend.api import routers
from backend.auth import auth_router
from logger import init_logger


app = FastAPI(title="Bug Tracker")
# create logger
init_logger(os.path.abspath(os.path.join(os.path.curdir, "logs", "bug_tracker.log")))

# define routers
app.include_router(routers, prefix="/api/v1")
app.include_router(auth_router, tags=["Auth"], prefix="/auth")


# create logger
init_logger(os.path.abspath(os.path.join(os.path.curdir, "logs", "bug_tracker.log")))
