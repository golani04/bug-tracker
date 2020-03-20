import pytest
from backend.models.projects import Project


_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2

# TODO: In order to speed up the tests, mock DB and check only API
@pytest.mark.api
def test_projects_get(app):
    response = app.get("/api/v0/projects")

    assert response.status_code == 200

    json = response.get_json()
    assert set(json[0]) >= {"name", "id", "maintainer", "favorite", "created", "updated"}


@pytest.mark.api
def test_create_project(app):
    length = len(Project.get_all_projects())
    response = app.post(
        "/api/v0/projects",
        json={
            "name": "Test through an API.",
            "maintainer": _MAINTAINER_ID,
            "description": "Any description",
        },
    )

    assert response.status_code == 201

    projects = Project.get_all_projects()
    assert length + 1 == len(projects)

    project_api = response.get_json()
    assert any([True for project in projects if project.id == project_api["id"]])


@pytest.mark.api
@pytest.mark.parametrize(
    "data, expected",
    [
        ({"json": {}}, "Received json is empty."),
        (
            {
                "data": {
                    "name": "Test through an API.",
                    "maintainer": _MAINTAINER_ID,
                    "description": "Any description",
                }
            },
            "Provided data is not a json.",
        ),
        (
            {"json": {"maintainer": _MAINTAINER_ID, "description": "Any description"}},
            "Missing required key: name.",
        ),
        (
            {"json": {"name": "Test through an API.", "description": "Any description"}},
            "Missing required key: maintainer.",
        ),
        ({"json": {"description": "Any description"}}, "Missing required keys: maintainer, name."),
        (
            {
                "json": {
                    "name": "Test through an API.",
                    "maintainer": _MAINTAINER_ID,
                    "description": "Any description",
                }
            },
            "Internal Server Error",
        ),
    ],
)
def test_create_project_failed(data, expected, app, monkeypatch):
    monkeypatch.setattr(Project, "save", lambda _: False)
    response = app.post("/api/v0/projects", **data)
    assert response.status_code in {400, 500}

    error = response.get_json()
    assert error["message"] == expected


def test_get_project(app, monkeypatch):
    monkeypatch.setattr(
        Project,
        "find_by_id",
        lambda _: Project(
            _PROJECT_ID,
            "test project",
            _MAINTAINER_ID,
            "Monkeypatch a project to test api responses",
        ),
    )
    response = app.get(f"/api/v0/projects/{_PROJECT_ID}")

    assert response.status_code == 200
    project = response.get_json()
    assert project is not None
    assert project["id"] == _PROJECT_ID


def test_get_project_failed(app, monkeypatch):
    monkeypatch.setattr(
        Project, "find_by_id", lambda _: None,
    )
    response = app.get(f"/api/v0/projects/{_PROJECT_ID}")

    assert response.status_code == 404
    project = response.get_json()
    assert project["message"] == "Required project is missing"
