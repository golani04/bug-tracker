from functools import lru_cache
from typing import Tuple

from jose.constants import Algorithms
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Bug Tracker"
    sqlalchemy_database_url: str
    debug: bool
    admin_user: str
    admin_pass: str
    admin_email: str
    AUTH_HEADERS: Tuple[str] = ("cookie",)
    COOKIE_HEADER_NAME: str = "access_token_cookie"
    SECRET_KEY: str
    ALGORITHM: str = Algorithms.HS256
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
