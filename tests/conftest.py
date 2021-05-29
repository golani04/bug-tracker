from contextlib import closing
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.db import Base, get_db
from main import app


engine = create_engine(
    "sqlite+pysqlite:///:memory:", echo=True, future=True, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create all tables
Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    with closing(TestingSessionLocal()) as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def session() -> Generator:
    sess = TestingSessionLocal()

    yield sess

    sess.close()


@pytest.fixture(scope="module")
def app() -> Generator:
    with TestClient(app) as client:
        yield client
