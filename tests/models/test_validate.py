from datetime import date, datetime
from enum import Enum

import pytest
from backend.models import validate


EnumObj = Enum("EnumObj", "one two three")
AnotherTestEnum = Enum("AnotherTestEnum", "one two three")


def test_validate_enum():
    assert validate.is_enum_has_prop(EnumObj, 1)
    assert validate.is_enum_has_prop(EnumObj, EnumObj.one)


@pytest.mark.parametrize("value", ["asdfasdf", "1", 4, AnotherTestEnum.one])
def test_validate_enum_fail(value):
    with pytest.raises(validate.ValidationError):
        validate.is_enum_has_prop(EnumObj, value)


test_id = "123456abcdefghijklmnopqrstuvwxyz" * 2


def test_validate_id():
    assert validate.item_id(test_id)


@pytest.mark.parametrize(
    "id_",
    [
        1234567890,  # number
        True,  # bool
        1 + 2j,  # complex
        (num for num in range(64)),  # generator
        [num for num in range(64)],  # list
        tuple(num for num in range(64)),  # tuple
        {num for num in range(64)},  # set
        {num: num for num in range(64)},  # dict
    ],
)
def test_validate_id_fail_not_str(id_):
    with pytest.raises(validate.ValidationError) as excinfo:
        validate.item_id(id_)
    assert str(excinfo.value) == "ID should be of type string."


@pytest.mark.parametrize(
    "value, err_msg",
    [
        ("abcdefghijklmn<(" * 4, "Has non-alphnumeric values."),
        (f"{'abcdefgr' * 8}1", "Invalid ID length."),  # len 65
        (("abcdefgr" * 8)[0:-1], "Invalid ID length."),  # len 63
    ],
)
def test_validate_id_fail_not_alphanumeric(value, err_msg):
    with pytest.raises(validate.ValidationError) as excinfo:
        validate.item_id(value)
    assert str(excinfo.value) == err_msg


@pytest.mark.parametrize("date_", ["2020-04-01", date(2020, 4, 1)])
def test_date(date_):
    assert validate.is_date(date_)


@pytest.mark.parametrize("date_", ["2020-13-01", "sadfsd", (2020, 1, 1)])
def test_date_fail(date_):
    with pytest.raises(validate.ValidationError):
        validate.is_date(date_)


@pytest.mark.parametrize("datetime_", ["2020-04-01 18:00:00", datetime(2020, 4, 1, 18, 0, 0)])
def test_datetime(datetime_):
    assert validate.is_datetime(datetime_)


@pytest.mark.parametrize(
    "datetime_", ["2020-13-01 18:00:00", "2020-01-01 25:00:00", "sadfsd", (2020, 1, 1)]
)
def test_datetime_fail(datetime_):
    with pytest.raises(validate.ValidationError):
        validate.is_datetime(datetime_)


@pytest.mark.parametrize("num", [1, 1.1, 0, 0.2, False])
def test_numeric(num):
    assert validate.is_numeric(num)


@pytest.mark.parametrize("num", ["1", "False", [], {}, (1,)])
def test_numeric_fail(num):
    with pytest.raises(validate.ValidationError):
        validate.is_numeric(num)