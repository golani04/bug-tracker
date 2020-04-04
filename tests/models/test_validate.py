import pytest
from backend.models import validate


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
