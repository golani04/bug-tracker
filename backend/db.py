from contextlib import closing
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import settings


# connect_args only requires by SQLite database, by default it prevents accessing db from different
# thread in order to prevent accidental sharing of the same connection
engine = create_engine(settings.sqlalchemy_database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    with closing(SessionLocal()) as db:
        yield db
