import pytest
from backend.models import util
from backend.models.users import User


_USER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2
_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2


def get_demo_user(*args, **kwargs):
    return User(
        _USER_ID,
        "Tester>",
        "test@&12345",
        "tester@gmail.com",
        util.hash_password("password"),
        _PROJECT_ID,
        type=5,
    )


@pytest.fixture
def mock_model_methods(monkeypatch):
    for prop in ["find_by_id", "modify", "delete"]:
        monkeypatch.setattr(User, prop, get_demo_user)


@pytest.fixture
def mock_model_save(monkeypatch):
    monkeypatch.setattr(User, "save", lambda *_: False)


@pytest.mark.api
def test_users_get(app):
    response = app.get("/api/v0/users")
    assert response.status_code == 200

    json = response.get_json()
    assert set(json[0]) >= {"name", "id", "password", "username", "created", "email", "type"}


@pytest.mark.api
def test_create_user(app):
    length = len(User.get_all())
    response = app.post(
        "/api/v0/users",
        json={
            "name": "Test",
            "username": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "project": _PROJECT_ID,
            "type": 5,
        },
    )

    assert response.status_code == 201

    users = User.get_all()
    assert length + 1 == len(users)

    user_api = response.get_json()
    assert any([True for user_id in users if user_id == user_api["id"]])


@pytest.mark.api
@pytest.mark.parametrize(
    "data, expected",
    [
        ({"json": {}}, "Received json is empty."),
        (
            {
                "data": {
                    "name": "Test",
                    "username": "tester",
                    "email": "tester@gmail.com",
                    "password": "password",
                    "project": _PROJECT_ID,
                    "type": 5,
                }
            },
            "Provided data is not a json.",
        ),
        (
            {
                "json": {
                    "username": "tester",
                    "email": "tester@gmail.com",
                    "password": "password",
                    "project": _PROJECT_ID,
                    "type": 5,
                }
            },
            "Missing required key: name.",
        ),
        (
            {
                "json": {
                    "name": "Test",
                    "username": "tester",
                    "email": "tester@gmail.com",
                    "project": _PROJECT_ID,
                }
            },
            "Missing required key: password.",
        ),
        (
            {"json": {"username": "tester", "email": "tester@gmail.com"}},
            "Missing required keys: name, password, project.",
        ),
    ],
)
def test_create_user_failed(data, expected, app, mock_model_save):
    response = app.post("/api/v0/users", **data)
    assert response.status_code == 400

    error = response.get_json()
    assert error["message"] == expected


@pytest.mark.api
def test_get_user(app, mock_model_methods):
    response = app.get(f"/api/v0/users/{_USER_ID}")

    assert response.status_code == 200
    user = response.get_json()
    assert user is not None
    assert user["id"] == _USER_ID


@pytest.mark.api
def test_modify_users(app, mock_model_methods):
    response = app.patch(f"/api/v0/users/{_USER_ID}", json={"name": "New name"})

    assert response.status_code == 200


@pytest.mark.api
def test_user_delete(app, mock_model_methods):
    response = app.delete(f"/api/v0/users/{_USER_ID}")
    assert response.status_code == 204


@pytest.mark.api
@pytest.mark.parametrize(
    "action,args,kwargs",
    [
        ("patch", (f"/api/v0/users/{_USER_ID}",), {"json": {"name": "404 Test"}}),
        ("get", (f"/api/v0/users/{_USER_ID}",), {}),
        ("delete", (f"/api/v0/users/{_USER_ID}",), {}),
    ],
)
def test_project_404(action, args, kwargs, app, monkeypatch):
    monkeypatch.setattr(User, "find_by_id", lambda *_: None)
    actions = {"patch": app.patch, "delete": app.delete, "get": app.get}
    response = actions[action](*args, **kwargs)

    assert response.status_code == 404
    assert response.get_json()["message"] == "Required user is missing"


@pytest.mark.api
@pytest.mark.parametrize(
    "action,args,kwargs",
    [
        (
            "post",
            (f"/api/v0/users",),
            {
                "json": {
                    "name": "Test",
                    "username": "tester",
                    "email": "tester@gmail.com",
                    "password": "password",
                    "project": _PROJECT_ID,
                    "type": 5,
                }
            },
        ),
        ("patch", (f"/api/v0/users/{_USER_ID}",), {"json": {"name": "Test a user updates"}}),
        ("delete", (f"/api/v0/users/{_USER_ID}",), {}),
    ],
)
def test_project_500(action, args, kwargs, app, mock_model_methods, mock_model_save):
    # an error produce by the database
    actions = {"patch": app.patch, "delete": app.delete, "post": app.post}
    response = actions[action](*args, **kwargs)

    assert response.status_code == 500
    assert response.get_json()["message"] == "Internal Server Error"
