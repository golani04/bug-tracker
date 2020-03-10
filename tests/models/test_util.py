import pytest
from backend.models import validate
from backend.models.util import create_id


@pytest.mark.xfail
def test_to_show_to_compare_each_with_each():
    id0 = 1
    id1 = 2
    id2 = 1

    assert id0 != id1 != id2  # true
    assert id0 != id2  # false


# see why using 2 asserts, see previous test
def test_create_random_ids():
    id0 = create_id()
    id1 = create_id()
    id2 = create_id()

    assert id0 != id1 != id2
    assert id0 != id2


def test_create_id_is_valid():
    assert validate.item_id(create_id())


def test_create_id_not_valid_pass_num():
    with pytest.raises(validate.ValidationError) as excinfo:
        validate.item_id(0)

    assert set(excinfo.value.args[0]) == {"ID should be of type string.", "Invalid ID length."}


def test_create_id_not_valid_not_alphnumeric():
    with pytest.raises(validate.ValidationError) as excinfo:
        validate.item_id("12345adfgasg-")

    assert set(excinfo.value.args[0]) == {"Has non-alphnumeric values.", "Invalid ID length."}
