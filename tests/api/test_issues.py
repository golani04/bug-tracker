import pytest

from backend.models.issues import Issue

_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2
_ISSUE_ID = "561234abcdefghijklmnopqrstuvwxyz"[::-1] * 2


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
        (
            # if save returns false
            {
                "json": {
                    "reporter": _MAINTAINER_ID,
                    "assignee": _MAINTAINER_ID,
                    "project": _PROJECT_ID,
                    "title": "Test save method",
                }
            },
            "Internal Server Error",
        ),
    ],
)
def test_create_issue_failed(data, expected, app, monkeypatch):
    # 500: an error produce by the database
    monkeypatch.setattr(Issue, "save", lambda *_: False)
    response = app.post("/api/v0/issues", **data)
    assert response.status_code in {400, 500}

    error = response.get_json()
    assert error["message"] == expected


@pytest.fixture
def find_by_id(monkeypatch):
    monkeypatch.setattr(
        Issue,
        "find_by_id",
        lambda _: Issue(
            **{
                "id": _ISSUE_ID,
                "title": "Create Issue from API",
                "reporter": _MAINTAINER_ID,
                "assignee": _MAINTAINER_ID,
                "project": _PROJECT_ID,
                "description": "Monkeypatch an issue to test an API response",
            }
        ),
    )


@pytest.mark.api
def test_get_issue(app, find_by_id):
    response = app.get(f"/api/v0/issues/{_ISSUE_ID}")

    assert response.status_code == 200
    issue = response.get_json()
    assert issue is not None
    assert issue["id"] == _ISSUE_ID


@pytest.mark.api
def test_get_issue_failed(app, monkeypatch):
    monkeypatch.setattr(
        Issue, "find_by_id", lambda _: None,
    )
    response = app.get(f"/api/v0/issues/{_ISSUE_ID}")

    assert response.status_code == 404
    assert response.get_json()["message"] == "Required issue is missing"
