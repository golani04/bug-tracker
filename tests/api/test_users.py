import pytest


_PROJECT_ID: str = "1eabdc24-2773-455a-9163-d7bcf6742037"
_MAINTAINER_ID: str = "8bbeff13-9c88-4c73-b150-203d6d7c5784"


@pytest.mark.api
def test_users_get(client):
    response = client.get("/api/users")
    assert response.status_code == 200

    json = response.json()
    assert set(json[0]) >= {"created_at", "email", "id", "name", "type", "username"}
