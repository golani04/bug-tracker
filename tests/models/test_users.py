from datetime import date
from freezegun import freeze_time
import pytest
from backend.models import validate
from backend.models.users import User, UserType

_USER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2


@freeze_time("2020-01-01")
def test_user_class():
    user = User(_USER_ID, "Tester>", "test@&12345", "tester@gmail.com", "password", type=5)
    assert user.type == UserType(5)
    assert user.name == "Tester&gt;"
    assert user.username == "test@&amp;12345"
    assert user.created == date(2020, 1, 1)


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
        User(id_, "Tester", "test", email, "password", type=type_)

    assert str(excinfo.value) == err
