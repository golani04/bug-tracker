import os

from functools import lru_cache

from pydantic import BaseSettings, main


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    app_name: str = "Bug Tracker"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
