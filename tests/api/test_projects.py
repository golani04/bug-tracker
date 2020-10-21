import pytest


_PROJECT_ID: str = "1eabdc24-2773-455a-9163-d7bcf6742037"
_MAINTAINER_ID: str = "8bbeff13-9c88-4c73-b150-203d6d7c5784"
_ISSUE_ID: int = 1


@pytest.mark.api
def test_get_projects(client):
    response = client.get("/api/projects")
    assert response.status_code == 200

    json = response.json()
    assert set(json[0]) >= {"created_at", "favorite", "id", "maintainer", "name", "updated_at"}
