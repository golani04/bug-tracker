from datetime import timedelta
from enum import Enum

import pytest
from backend.models import validate
from backend.models import util


@pytest.mark.xfail
def test_to_show_to_compare_each_with_each():
    id0 = 1
    id1 = 2
    id2 = 1

    assert id0 != id1 != id2  # true
    assert id0 != id2  # false


# see why using 2 asserts, see previous test
def test_create_random_ids():
    id0 = util.create_id()
    id1 = util.create_id()
    id2 = util.create_id()

    assert id0 != id1 != id2
    assert id0 != id2


def test_create_id_is_valid():
    assert validate.item_id(util.create_id())


EnumObj = Enum("EnumObj", "one two three")


@pytest.mark.parametrize("value, expected", [(EnumObj.one, EnumObj.one), (1, EnumObj.one)])
def test_value_to_enum(value, expected):
    assert util.value_to_enum(EnumObj, value) == expected


def test_value_to_enum_fails():
    with pytest.raises(ValueError) as excinfo:
        util.value_to_enum(EnumObj, "1")

    assert str(excinfo.value) == "'1' is not a valid EnumObj"


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            timedelta(days=25, hours=26, minutes=80, seconds=1000),
            {"weeks": 3, "days": 5, "hours": 3, "minutes": 36, "seconds": 40},
        ),
        (
            timedelta(hours=1, seconds=1),
            {"weeks": 0, "days": 0, "hours": 1, "minutes": 0, "seconds": 1},
        ),
    ],
)
def test_td_convertion_to_wdhms(value, expected):
    assert util.seconds_to_wdhms(value) == expected


def test_td_convertion_fails():
    value = 18000
    with pytest.raises(ValueError) as excinfo:
        util.seconds_to_wdhms(value)

    assert str(excinfo.value) == (
        f"Incorrect type of variable is passed. Provided type: {type(value)} "
        "and should be of timedelta type."
    )


@pytest.mark.parametrize(
    "wdhms",
    [
        {"weeks": 2},
        {"weeks": 0, "days": 5, "minutes": 17},
        {"weeks": 0, "days": 35, "seconds": 10},
        100,
        0,
        1001,
    ],
)
def test_wdhms_to_seconds(wdhms):
    times = {
        "week": 7 * 24 * 60 * 60,
        "day": 24 * 60 * 60,
        "hour": 60 * 60,
        "minute": 60,
        "second": 1,
    }
    expected = (
        sum((times[k[:-1]] * v for k, v in wdhms.items())) if isinstance(wdhms, dict) else wdhms
    )

    assert util.wdhms_to_seconds(wdhms) == expected
