import os
from backend.db import _save_json, _read_json


def test_save_json_failed():
    is_saved = _save_json(os.path.join("non-existing-json", "any.json"), ["Any", "data"])

    assert is_saved is False


def test_read_json_failed():
    data = _read_json(os.path.join("non-existing-json", "any.json"))

    assert data == []
