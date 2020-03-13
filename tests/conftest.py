import json
import pytest
from collections import namedtuple
from typing import NamedTuple

from backend import create_app
from tests.data import projects


@pytest.fixture(scope="session")
def test_config() -> NamedTuple:
    return namedtuple("TestConfig", "PROJECTS_PATH")


@pytest.fixture(scope="session")
def tmp_config(tmpdir_factory, test_config: NamedTuple) -> NamedTuple:
    f_projects = tmpdir_factory.mktemp("projects").join("projects.json")
    f_projects.write(json.dumps(projects._data))

    return test_config(PROJECTS_PATH=f_projects)


@pytest.fixture
def app(tmp_config: NamedTuple):
    app = create_app(db_config=tmp_config)

    with app.test_client() as client:
        yield client
