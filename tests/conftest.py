import json
import pytest
from collections import namedtuple
from typing import NamedTuple

from backend import create_app
from tests.data import projects, issues


@pytest.fixture
def test_config() -> NamedTuple:
    return namedtuple("TestConfig", "PROJECTS_PATH ISSUES_PATH")


@pytest.fixture
def tmp_config(tmpdir_factory, test_config: NamedTuple) -> NamedTuple:
    # create propject json
    f_projects = tmpdir_factory.mktemp("projects").join("projects.json")
    f_projects.write(json.dumps(projects._data))
    # create issue json
    f_issues = tmpdir_factory.mktemp("issues").join("issues.json")
    f_issues.write(json.dumps(issues._data))

    return test_config(PROJECTS_PATH=f_projects, ISSUES_PATH=f_issues)


@pytest.fixture
def app(tmp_config: NamedTuple):
    app = create_app(db_config=tmp_config)

    with app.test_client() as client:
        yield client
