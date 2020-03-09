import json
import pytest
from backend import create_app
from tests.data import projects


@pytest.fixture
def app():
    app = create_app()

    with app.test_client() as client:
        yield client


@pytest.fixture
def projects_json(tmpdir_factory):
    f_projects = tmpdir_factory.mktemp("projects").join("projects.json")
    f_projects.write(json.dumps(projects._data))

    return f_projects
