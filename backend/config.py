from functools import lru_cache
from pathlib import Path
from typing import Tuple

from jose.constants import Algorithms
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent / ".env")

    app_name: str = "Bug Tracker"
    debug: bool
    admin_user: str
    admin_pass: str
    admin_email: str
    SQLALCHEMY_DATABASE_URL: str
    AUTH_HEADERS: Tuple[str] = ("cookie",)
    COOKIE_HEADER_NAME: str = "access_token_cookie"
    SECRET_KEY: str
    ALGORITHM: str = Algorithms.HS256
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
