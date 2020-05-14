import pytest
from backend.models.users import User

_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
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
            {"json": {"username": "tester", "email": "tester@gmail.com",}},
            "Missing required keys: name, password, project.",
        ),
    ],
)
def test_create_user_failed(data, expected, app, mock_model_save):
    response = app.post("/api/v0/users", **data)
    assert response.status_code == 400

    error = response.get_json()
    assert error["message"] == expected

