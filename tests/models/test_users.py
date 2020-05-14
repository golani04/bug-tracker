from datetime import date
from freezegun import freeze_time
import pytest
from backend.models import validate, util
from backend.models.users import User, UserType

_USER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2
_EXISTING_USER_ID = "f773f6953b0ca528aa6d874d93a479a1f14540cd6c4edb972c5faa7c6708cc17"
_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_EXISTING_PROJECT_ID = "c0e898915bd4f2c0fed3cf657609ce2e5ea885d2fbcf923393352962488b008c"


@freeze_time("2020-01-01")
def test_user_class():
    user = User(
        _USER_ID,
        "Tester>",
        "test@&12345",
        "tester@gmail.com",
        util.hash_password("password"),
        _PROJECT_ID,
        type=5,
    )
    assert user.type == UserType(5)
    assert user.name == "Tester&gt;"
    assert user.username == "test@&amp;12345"
    assert user.created == date(2020, 1, 1)
    assert user.password != "password"
    assert util.verify_password("password", user.password)


@pytest.mark.parametrize(
    "id_, email, type_, err",
    [
        (_USER_ID[0:-1], "asdf@example.com", 1, "Invalid ID length."),
        (_USER_ID, "asdf<[ef]>gh@example.com", 1, "Email is invalid: asdf<[ef]>gh@example.com"),
        (_USER_ID, "asdf@example.com", 6, "This <enum 'UserType'> is missing 6"),  # 1 <= type_ <= 5
    ],
)
def test_user_class_invalid(id_, email, type_, err):
    with pytest.raises(validate.ValidationError) as excinfo:
        User(id_, "Tester", "test", email, "password", _PROJECT_ID, type=type_)

    assert str(excinfo.value) == err


def test_get_all_users(app):
    users = User.get_all()

    assert users != []
    assert len(users) == 10


@freeze_time("2020-01-01")
def test_create_user():
    user = User.create(
        {
            "id": _USER_ID,
            "created": "2019-10-10",
            "name": "Test create",
            "username": "test@create",
            "email": "test@test.com",
            "password": "password",
            "project": _PROJECT_ID,
            "type": 3,
        }
    )

    assert user.id is not None
    assert user.id != _USER_ID
    assert user.created == date(2020, 1, 1)
    assert user.type == UserType.developer


def test_create_user_save(app):
    user = User.create(
        {
            "id": _USER_ID,
            "created": "2019-10-10",
            "name": "Test create",
            "username": "test@create",
            "email": "test@test.com",
            "password": "password",
            "project": _PROJECT_ID,
            "type": 3,
        }
    )

    user.save("create")
    users = User.get_all()
    assert users[user.id] == user
    assert len(users) == 11


def test_find_id(app):
    assert User.find_by_id(_PROJECT_ID) is None
    assert User.find_by_id(_EXISTING_USER_ID) is not None


def test_delete_user(app):
    user = User.find_by_id(_EXISTING_USER_ID)
    assert len(User.get_all()) == 10

    deleted_user = user.delete()
    user.save("delete")
    assert deleted_user.id == user.id
    assert len(User.get_all()) == 9


@freeze_time("2020-01-01")
@pytest.mark.parametrize(
    "prop, val, expected",
    [
        ("name", "Test create", "Test create"),
        ("username", "test@create", "test@create"),
        ("email", "test@test.com", "test@test.com"),
        ("type", 5, UserType(5)),
        # unchangeable keys
        ("id", _USER_ID, _EXISTING_USER_ID),
        ("project", _PROJECT_ID, _EXISTING_PROJECT_ID),
        ("created", "2019-10-10", date(2020, 1, 1)),
    ],
)
def test_modify_user(app, prop, val, expected):
    user = User.find_by_id(_EXISTING_USER_ID)
    user = user.modify({prop: val})

    assert getattr(user, prop) == expected


def test_modify_user_password(app):
    user = User.find_by_id(_EXISTING_USER_ID)
    passw = "new_password"
    user = user.modify({"password": passw})
    assert util.verify_password(passw, user.password)

    user.save("modify")
    user = User.get_all()[_EXISTING_USER_ID]
    assert util.verify_password(passw, user.password)
