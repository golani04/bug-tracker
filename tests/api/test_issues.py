import pytest


@pytest.mark.api
def test_issue_get_all(app):
    res = app.get("/api/v0/issues")
    assert res.status_code == 200

    data = res.get_json()
    assert set(data[0]) > {"id", "title", "created", "description", "assignee"}
