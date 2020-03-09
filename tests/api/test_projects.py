import pytest

from backend import db


@pytest.mark.api
def test_projects_get(app, projects_json):
    db._projects = projects_json
    response = app.get("/api/v0/projects")

    assert response.status_code == 200

    json = response.get_json()
    assert set(json[0]) >= {"name", "id", "maintainer", "favorite", "_created", "_updated"}
