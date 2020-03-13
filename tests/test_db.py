from backend import database as db
from backend.config import db_config


def test_create_projects(app):
    # check that reassign worked
    assert db.config.PROJECTS_PATH != db_config.PROJECTS_PATH

    projects = db.get_projects()
    assert isinstance(projects, list)
    assert len(projects) > 0
