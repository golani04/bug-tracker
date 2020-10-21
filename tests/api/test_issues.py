import pytest


_PROJECT_ID: str = "1eabdc24-2773-455a-9163-d7bcf6742037"
_MAINTAINER_ID: str = "8bbeff13-9c88-4c73-b150-203d6d7c5784"
_ISSUE_ID: int = 1


@pytest.mark.api
def test_get_issues(client):
    res = client.get("/api/issues")
    assert res.status_code == 200

    data = res.json()
    assert set(data[0]) >= {"assignee", "created_at", "description", "id", "title"}
