from backend.api.util import filter_unchangeable_keys

_DATA = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
}


def test_unchangeable_keys():
    func = filter_unchangeable_keys({"c", "a"})
    func = func(lambda project_id, data: data)
    filtered_data = func(_DATA, "project_id")

    assert set(filtered_data.keys()) == {"d", "b"}


def test_unchangeable_keys_are_empty():
    func = filter_unchangeable_keys()
    func = func(lambda project_id, data: data)
    unfiltered_data = func(_DATA, "project_id")

    assert unfiltered_data == _DATA
