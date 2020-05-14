import pytest
from backend.models.users import User

@pytest.mark.api
def test_users_get(app):
    response = app.get("/api/v0/users")
    assert response.status_code == 200

    json = response.get_json()
    assert set(json[0]) >= {"name", "id", "password", "username", "created", "email", "type"}
