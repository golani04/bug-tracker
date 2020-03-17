import pytest
from datetime import date, datetime
from freezegun import freeze_time

from backend import database as db
from backend.models.projects import Project
from backend.models.validate import ValidationError


_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2


@freeze_time("2020-01-01 12:01:01.123456")
def test_project():
    # GIVEN
    project = Project(_PROJECT_ID, "test", _MAINTAINER_ID, "Testing a project")
    # WHEN
    # set updated for some reason freezegun didn't work on datetime.utcnow
    project.updated = datetime.utcnow()  # like this it adds freeze time
    # THEN
    assert project.created == date.today() == date(2020, 1, 1)
    assert project.updated == datetime(2020, 1, 1, 12, 1, 1, 123456)
    assert project.id == _PROJECT_ID
    assert project.favorite is False  # default


def test_post_init_id_not_str():
    with pytest.raises(ValidationError):
        # id is not of type str
        Project(123456, "tes<t", _MAINTAINER_ID, "Testing a project")


def test_post_init_not_len():
    with pytest.raises(ValidationError):
        # id is not of type str
        Project(_PROJECT_ID[0:10], "tes<t", _MAINTAINER_ID, "Testing a project")


def test_post_init_escape_html_name():
    project = Project(_PROJECT_ID, "tes<t", _MAINTAINER_ID, "Testing a project")

    assert project.name == "tes&lt;t"


@freeze_time("2020-1-1")
def test_create_project():
    project = Project.create("Test project", _MAINTAINER_ID, "First create")

    assert isinstance(project, Project)
    assert project.created == date(2020, 1, 1)
    assert project.maintainer == _MAINTAINER_ID
    assert project.favorite is False


def test_maintainer_id_invalid():
    with pytest.raises(ValidationError):
        Project.create("Test project", "_MAINTAINER_ID", "First create")


def test_project_save(app):
    # GIVEN
    length = len(Project.get_all_projects())
    assert length > 0
    # WHEN
    project = Project(_PROJECT_ID, "tes<t", _MAINTAINER_ID, "Testing a project")
    # THEN
    assert project.save() is True
    assert len(Project.get_all_projects()) == length + 1


def test_project_failed(app, test_config):
    # GIVEN
    db.config = test_config(PROJECTS_PATH="/non-existing-tmp/projects.json")
    # WHEN
    project = Project(_PROJECT_ID, "tes<t", _MAINTAINER_ID, "Testing a project")
    # THEN
    assert project.save() is False
