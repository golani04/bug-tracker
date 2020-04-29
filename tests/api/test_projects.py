import pytest
from backend.models.projects import Project


_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2


@pytest.fixture
def find_by_id(monkeypatch):
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


@pytest.fixture
def del_project(find_by_id, monkeypatch):
    monkeypatch.setattr(
        Project,
        "delete",
        lambda _: Project(
            _PROJECT_ID,
            "test project",
            _MAINTAINER_ID,
            "Monkeypatch a project to test api responses",
        ),
    )


@pytest.fixture
def mod_project(find_by_id, monkeypatch):
    monkeypatch.setattr(
        Project,
        "modify",
        lambda *_: Project(
            _PROJECT_ID,
            "test project",
            _MAINTAINER_ID,
            "Monkeypatch a project to test api responses",
        ),
    )


@pytest.mark.api
def test_projects_get(app):
    response = app.get("/api/v0/projects")
    assert response.status_code == 200

    json = response.get_json()
    assert set(json[0]) >= {"name", "id", "maintainer", "favorite", "created", "updated"}


@pytest.mark.api
def test_create_project(app):
    length = len(Project.get_all())
    response = app.post(
        "/api/v0/projects",
        json={
            "name": "Test through an API.",
            "maintainer": _MAINTAINER_ID,
            "description": "Any description",
        },
    )

    assert response.status_code == 201

    projects = Project.get_all()
    assert length + 1 == len(projects)

    project_api = response.get_json()
    assert any([True for project_id in projects if project_id == project_api["id"]])


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
    # 500: an error produce by the database
    monkeypatch.setattr(Project, "save", lambda *_: False)
    response = app.post("/api/v0/projects", **data)
    assert response.status_code in {400, 500}

    error = response.get_json()
    assert error["message"] == expected


@pytest.mark.api
def test_get_project(app, find_by_id):
    response = app.get(f"/api/v0/projects/{_PROJECT_ID}")

    assert response.status_code == 200
    project = response.get_json()
    assert project is not None
    assert project["id"] == _PROJECT_ID


@pytest.mark.api
def test_get_project_failed(app, monkeypatch):
    monkeypatch.setattr(
        Project, "find_by_id", lambda _: None,
    )
    response = app.get(f"/api/v0/projects/{_PROJECT_ID}")

    assert response.status_code == 404
    project = response.get_json()
    assert project["message"] == "Required project is missing"


@pytest.mark.api
def test_project_delete(app, del_project):
    response = app.delete(f"/api/v0/projects/{_PROJECT_ID}")
    assert response.status_code == 204


@pytest.mark.api
def test_project_delete_404(app, monkeypatch):
    monkeypatch.setattr(Project, "find_by_id", lambda *_: None)
    response = app.delete(f"/api/v0/projects/{_PROJECT_ID}")

    assert response.status_code == 404
    assert response.get_json()["message"] == "Required project is missing"


@pytest.mark.api
def test_project_delete_500(app, del_project, monkeypatch):
    # an error produce by the database
    monkeypatch.setattr(Project, "save", lambda *_: False)
    response = app.delete(f"/api/v0/projects/{_PROJECT_ID}")

    assert response.status_code == 500
    assert response.get_json()["message"] == "Internal Server Error"


@pytest.mark.api
def test_modify_project(app, mod_project):
    response = app.patch(f"/api/v0/projects/{_PROJECT_ID}", json={"name": "New name"})

    assert response.status_code == 200


@pytest.mark.api
def test_project_modify_404(app, monkeypatch):
    monkeypatch.setattr(Project, "find_by_id", lambda *_: None)
    response = app.patch(f"/api/v0/projects/{_PROJECT_ID}", json={"name": "New name"})

    assert response.status_code == 404
    assert response.get_json()["message"] == "Required project is missing"


@pytest.mark.api
def test_project_modify_500(app, del_project, monkeypatch):
    # an error produce by the database
    monkeypatch.setattr(Project, "save", lambda *_: False)
    response = app.patch(f"/api/v0/projects/{_PROJECT_ID}", json={"name": "New name"})

    assert response.status_code == 500
    assert response.get_json()["message"] == "Internal Server Error"
