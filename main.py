import os

from fastapi import FastAPI

from backend.api import routers
from backend.auth import auth_routers
from backend.general import main_router
from logger import init_logger


app = FastAPI(title="Bug Tracker")


# define routers
app.include_router(routers, prefix="/api/v1")
app.include_router(auth_routers, prefix="/auth")
app.include_router(main_router)

# create logger
init_logger(os.path.abspath(os.path.join(os.path.curdir, "logs", "bug_tracker.log")))
