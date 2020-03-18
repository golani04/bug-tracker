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
    # set `updated` manually, `freezegun` didn't work on `datetime.utcnow`
    # this assignment will set value to the value provided in decorator `@freeze_time`
    project.updated = datetime.utcnow()
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


def test_get_projects_are_cached(app):
    # GIVEN
    get_projects = Project.get_all_projects
    cache_info = get_projects.cache_info
    # clear cache before tests
    get_projects.cache_clear()
    # WHEN
    get_projects()
    info = cache_info()
    # THEN
    assert info.hits == 0

    # WHEN
    get_projects()
    info = cache_info()
    # THEN
    assert info.hits == 1


def test_that_cached_cleared(app):
    # GIVEN
    get_projects = Project.get_all_projects
    cache_info = get_projects.cache_info
    # WHEN
    get_projects()
    get_projects()
    info = cache_info()
    # THEN
    assert info.hits > 0
    # WHEN
    project = Project.create("Test project", _MAINTAINER_ID, "First create")
    project.save()
    info = cache_info()
    # THEN
    assert info.hits == 0


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


def test_find_project(app):
    project = Project.find_by_id("c0e898915bd4f2c0fed3cf657609ce2e5ea885d2fbcf923393352962488b008c")
    assert project is not None


def test_find_project_failed(app):
    project = Project.find_by_id("non-ex1sting-project-1")
    assert project is None
