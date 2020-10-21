import pytest
from fastapi.testclient import TestClient

from main import app
from backend.db import FileDatabase
from tests.data import issues, projects, users


@pytest.fixture
def mock_db_json(monkeypatch):
    def mock_projects(*args, **kwargs):
        return projects._data

    def mock_issues(*args, **kwargs):
        return issues._data

    def mock_users(*args, **kwargs):
        return users._data

    monkeypatch.setattr(FileDatabase, "get_projects", mock_projects)
    monkeypatch.setattr(FileDatabase, "get_issues", mock_issues)
    monkeypatch.setattr(FileDatabase, "get_users", mock_users)


@pytest.fixture
def client(mock_db_json):
    yield TestClient(app)
