import pytest
from backend.models.issues import Issue

_PROJECT_ID: str = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID: str = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2
_ISSUE_ID: str = "561234abcdefghijklmnopqrstuvwxyz"[::-1] * 2


@pytest.mark.api
def test_issue_get_all(app):
    res = app.get("/api/v0/issues")
    assert res.status_code == 200

    data = res.get_json()
    assert set(data[0]) > {"id", "title", "created", "description", "assignee"}


@pytest.mark.api
def test_create_issue(app):
    length = len(Issue.get_all())
    response = app.post(
        "/api/v0/issues",
        json={
            "title": "Create Issue from API",
            "reporter": _MAINTAINER_ID,
            "assignee": _MAINTAINER_ID,
            "project": _PROJECT_ID,
            "description": "Some Description",
        },
    )

    assert response.status_code == 201

    issues = Issue.get_all()
    assert length + 1 == len(issues)

    issue_from_api = response.get_json()
    assert any(True for issue_id in issues if issue_id == issue_from_api["id"])


@pytest.mark.api
@pytest.mark.parametrize(
    "data, expected",
    [
        ({"json": {}}, "Received json is empty."),
        (
            {
                "data": {
                    "title": "Test through an API.",
                    "assignee": _MAINTAINER_ID,
                    "description": "Any description",
                }
            },
            "Provided data is not a json.",
        ),
        (
            {"json": {"reporter": _MAINTAINER_ID, "description": "Any description"}},
            "Missing required keys: assignee, project, title.",
        ),
        (
            {
                "json": {
                    "reporter": _MAINTAINER_ID,
                    "assignee": _MAINTAINER_ID,
                    "project": _PROJECT_ID,
                    "description": "Any description",
                }
            },
            "Missing required key: title.",
        ),
    ],
)
def test_create_issue_failed(data, expected, app):
    response = app.post("/api/v0/issues", **data)

    assert response.status_code == 400
    assert response.get_json()["message"] == expected


def get_demo_issue(*args, **kwargs):
    return Issue(
        **{
            "id": _ISSUE_ID,
            "title": "Create Issue from API",
            "reporter": _MAINTAINER_ID,
            "assignee": _MAINTAINER_ID,
            "project": _PROJECT_ID,
            "description": "Monkeypatch an issue to test an API response",
        }
    )


@pytest.fixture
def mock_model_methods(monkeypatch):
    for prop in ["find_by_id", "delete", "modify"]:
        monkeypatch.setattr(Issue, prop, get_demo_issue)


@pytest.mark.api
def test_get_issue(app, mock_model_methods):
    response = app.get(f"/api/v0/issues/{_ISSUE_ID}")

    assert response.status_code == 200
    issue = response.get_json()
    assert issue is not None
    assert issue["id"] == _ISSUE_ID


@pytest.mark.api
def test_issue_delete(app, mock_model_methods):
    response = app.delete(f"/api/v0/issues/{_ISSUE_ID}")
    assert response.status_code == 204


@pytest.mark.api
def test_issue_modify(app, mock_model_methods):
    response = app.patch(
        f"/api/v0/issues/{_ISSUE_ID}", json={"title": "Test an issue modification"}
    )

    assert response.status_code == 200


@pytest.mark.api
@pytest.mark.parametrize(
    "action,args,kwargs",
    [
        (
            "patch",
            (f"/api/v0/issues/{_ISSUE_ID}",),
            {"json": {"title": "Test an issue modification"}},
        ),
        ("get", (f"/api/v0/issues/{_ISSUE_ID}",), {}),
        ("delete", (f"/api/v0/issues/{_ISSUE_ID}",), {}),
    ],
)
def test_issue_modify_404(action, args, kwargs, app, monkeypatch):
    monkeypatch.setattr(Issue, "find_by_id", lambda *_: None)
    actions = {"patch": app.patch, "delete": app.delete, "get": app.get, "post": app.post}
    response = actions[action](*args, **kwargs)

    assert response.status_code == 404
    assert response.get_json()["message"] == "Required issue is missing"


@pytest.mark.api
@pytest.mark.parametrize(
    "action,args,kwargs",
    [
        (
            "post",
            (f"/api/v0/issues",),
            {
                "json": {
                    "reporter": _MAINTAINER_ID,
                    "assignee": _MAINTAINER_ID,
                    "project": _PROJECT_ID,
                    "title": "Test save method",
                }
            },
        ),
        (
            "patch",
            (f"/api/v0/issues/{_ISSUE_ID}",),
            {"json": {"title": "Test an issue modification"}},
        ),
        ("delete", (f"/api/v0/issues/{_ISSUE_ID}",), {}),
    ],
)
def test_issue_500(action, args, kwargs, app, mock_model_methods, monkeypatch):
    # an error produce by the database
    monkeypatch.setattr(Issue, "save", lambda *_: False)
    actions = {"patch": app.patch, "delete": app.delete, "post": app.post}
    response = actions[action](*args, **kwargs)

    assert response.status_code == 500
    assert response.get_json()["message"] == "Internal Server Error"
