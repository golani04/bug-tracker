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
