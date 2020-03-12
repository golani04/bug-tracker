import pytest

from backend import database as db


_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2


@pytest.mark.api
def test_projects_get(app):
    response = app.get("/api/v0/projects")

    assert response.status_code == 200

    json = response.get_json()
    assert set(json[0]) >= {"name", "id", "maintainer", "favorite", "_created", "_updated"}


@pytest.mark.api
def test_create_prject(app):
    response = app.post(
        "/api/v0/projects",
        json={
            "name": "Test through an API.",
            "maintainer": _MAINTAINER_ID,
            "description": "Any description",
        },
    )

    assert response.status_code == 201
    assert 0
