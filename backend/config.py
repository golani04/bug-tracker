import os
from pydantic import BaseSettings
from backend.logger import init_logger


_logger = init_logger(os.path.abspath(os.path.join(os.path.curdir, "logs", "back-tracker.log")))


class Settings(BaseSettings):
    app_name = "Bug Tracker"
    logger = _logger
    users_path = os.path.abspath(os.path.join(os.path.curdir, "db_files", "users", "users.json"))
    projects_path = os.path.abspath(
        os.path.join(os.path.curdir, "db_files", "projects", "projects.json")
    )
    issues_path = os.path.abspath(os.path.join(os.path.curdir, "db_files", "issues", "issues.json"))

    class Config:
        env_file = ".env"


settings = Settings()
