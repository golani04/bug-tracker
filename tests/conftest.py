import json
import pytest
from _pytest.tmpdir import TempdirFactory
from collections import namedtuple
from functools import partial
from typing import types, NamedTuple

from backend import create_app, models
from tests.data import projects, issues, users


@pytest.fixture
def test_config() -> NamedTuple:
    return namedtuple("TestConfig", "PROJECTS_PATH ISSUES_PATH USERS_PATH")


def set_path(td: TempdirFactory, module: types.ModuleType):
    name = module.__name__.split(".")[-1]
    f_path = td.mktemp(name).join(f"{name}.json")
    f_path.write(json.dumps(module._data))

    return f_path


@pytest.fixture
def tmp_config(tmpdir_factory, test_config: NamedTuple) -> NamedTuple:
    _set_path = partial(set_path, tmpdir_factory)
    return test_config(
        PROJECTS_PATH=_set_path(projects),
        ISSUES_PATH=_set_path(issues),
        USERS_PATH=_set_path(users),
    )


@pytest.fixture
def app(tmp_config: NamedTuple):
    app = create_app(db_config=tmp_config)

    with app.test_client() as client:
        yield client

    models.projects.Project.get_all.cache_clear()
    models.issues.Issue.get_all.cache_clear()
