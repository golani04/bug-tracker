import json
import pytest
from tests.data import projects


@pytest.fixture
def projects_json(tmpdir_factory):
    f_projects = tmpdir_factory.mktemp("projects").join("projects.json")
    f_projects.write(json.dumps(projects._data))

    return f_projects
