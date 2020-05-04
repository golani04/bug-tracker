import pytest
from backend.models.projects import Project


_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2


def get_demo_project(*args, **kwargs):
    return Project(
        _PROJECT_ID,
        "test project",
        _MAINTAINER_ID,
        "Monkeypatch a project to test an API responses",
    )


@pytest.fixture
def mock_model_methods(monkeypatch):
    for prop in ["find_by_id", "modify", "delete"]:
        monkeypatch.setattr(Project, prop, get_demo_project)
    monkeypatch.setattr(Project, "get_issues", list)


@pytest.fixture
def mock_model_save(monkeypatch):
    monkeypatch.setattr(Project, "save", lambda *_: False)


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
def test_create_project_failed(data, expected, app, mock_model_save):
    # 500: an error produce by the database
    response = app.post("/api/v0/projects", **data)
    assert response.status_code in {400, 500}

    error = response.get_json()
    assert error["message"] == expected


@pytest.mark.api
def test_get_project(app, mock_model_methods):
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
def test_project_delete(app, mock_model_methods):
    response = app.delete(f"/api/v0/projects/{_PROJECT_ID}")
    assert response.status_code == 204


@pytest.mark.api
def test_project_delete_404(app, monkeypatch):
    monkeypatch.setattr(Project, "find_by_id", lambda *_: None)
    response = app.delete(f"/api/v0/projects/{_PROJECT_ID}")

    assert response.status_code == 404
    assert response.get_json()["message"] == "Required project is missing"


@pytest.mark.api
def test_project_delete_500(app, mock_model_methods, mock_model_save):
    # an error produce by the database
    response = app.delete(f"/api/v0/projects/{_PROJECT_ID}")

    assert response.status_code == 500
    assert response.get_json()["message"] == "Internal Server Error"


@pytest.mark.api
def test_modify_project(app, mock_model_methods):
    response = app.patch(f"/api/v0/projects/{_PROJECT_ID}", json={"name": "New name"})

    assert response.status_code == 200


@pytest.mark.api
def test_project_modify_404(app, monkeypatch):
    monkeypatch.setattr(Project, "find_by_id", lambda *_: None)
    response = app.patch(f"/api/v0/projects/{_PROJECT_ID}", json={"name": "New name"})

    assert response.status_code == 404
    assert response.get_json()["message"] == "Required project is missing"


@pytest.mark.api
def test_project_modify_500(app, mock_model_methods, mock_model_save):
    # an error produce by the database
    response = app.patch(f"/api/v0/projects/{_PROJECT_ID}", json={"name": "New name"})

    assert response.status_code == 500
    assert response.get_json()["message"] == "Internal Server Error"


@pytest.mark.api
def test_project_get_issues(app, mock_model_methods):
    response = app.get(f"/api/v0/projects/{_PROJECT_ID}/issues")

    assert response.status_code == 200
    assert response.get_json() == []
