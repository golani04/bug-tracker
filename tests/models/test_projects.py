import pytest
from datetime import date, datetime
from freezegun import freeze_time

from backend.models.issues import Issue
from backend.models.projects import Project
from backend.models.validate import ValidationError


_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2
_EXISTING_PROJECT = "c0e898915bd4f2c0fed3cf657609ce2e5ea885d2fbcf923393352962488b008c"


@freeze_time("2020-01-01 12:01:01.123456")
def test_project():
    # GIVEN
    project = Project(_PROJECT_ID, "test", _MAINTAINER_ID, "Testing a project")
    # WHEN
    # set `updated_at` manually, `freezegun` failed on `datetime.utcnow`
    # this assignment will set value to the value provided in decorator `@freeze_time`
    project.updated_at = datetime.utcnow()
    # THEN
    assert project.created_at == date.today() == date(2020, 1, 1)
    assert project.updated_at == datetime(2020, 1, 1, 12, 1, 1, 123456)
    assert project.id == _PROJECT_ID
    assert project.favorite is False  # default


def test_post_init_escape_html_name():
    project = Project(_PROJECT_ID, "tes<t", _MAINTAINER_ID, "Testing a project")

    assert project.name == "tes&lt;t"


def test_get_projects_are_cached(app):
    # GIVEN
    get_projects = Project.get_all
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
    get_projects = Project.get_all
    cache_info = get_projects.cache_info
    # WHEN
    get_projects()
    # second time in order to test that function takes data from cache
    get_projects()
    info = cache_info()
    # THEN
    assert info.hits > 0
    # WHEN
    project = Project.create(
        {"name": "Test project", "maintainer": _MAINTAINER_ID, "description": "First create"}
    )
    project.save("create")
    info = cache_info()
    # THEN
    assert info.hits == 0


@freeze_time("2020-1-1")
def test_create_project():
    project = Project.create(
        {"name": "Test project", "maintainer": _MAINTAINER_ID, "description": "First create"}
    )

    assert isinstance(project, Project)
    assert project.created_at == date(2020, 1, 1)
    assert project.maintainer == _MAINTAINER_ID
    assert project.favorite is False


def test_maintainer_id_invalid():
    with pytest.raises(ValidationError):
        Project.create(
            {"name": "Test project", "maintainer": "not_a_valid_id", "description": "First create"}
        )


def test_project_save(app):
    # GIVEN
    length = len(Project.get_all())
    assert length > 0
    # WHEN
    project = Project(_PROJECT_ID, "tes<t", _MAINTAINER_ID, "Testing a project")
    # THEN
    assert project.save("create") is True
    assert len(Project.get_all()) == length + 1


def test_find_project(app):
    project = Project.find_by_id(_EXISTING_PROJECT)
    assert project is not None


def test_find_project_failed(app):
    project = Project.find_by_id("non-ex1sting-project-1")
    assert project is None


def test_delete_project(app):
    project = Project.find_by_id(_EXISTING_PROJECT)
    assert project.delete() is not None
    assert any(project_id == project.id for project_id in Project.get_all()) is False


@freeze_time("2020-01-01 12:00:00.1234")
def test_modify_project(app):
    # GIVEN
    project = Project(_PROJECT_ID, "tes<t", _MAINTAINER_ID, "Testing a project")
    prev_name = project.name
    prev_description = project.description
    # WHEN
    updated_project = project.modify(
        {"name": "Name is changed", "description": "New desc for a project"}
    )
    # THEN
    assert project is not updated_project
    assert prev_name == "tes&lt;t"
    assert prev_name != updated_project.name
    assert prev_description == "Testing a project"
    assert prev_description != updated_project.description
    assert updated_project.updated_at == datetime(2020, 1, 1, 12, 0, 0, 123400)


def test_modify_project_id_is_not_changed(app):
    # GIVEN
    project = Project(_PROJECT_ID, "tes<t", _MAINTAINER_ID, "Testing a project")
    # WHEN
    updated_project = project.modify({"id": "a" * 64})
    # THEN
    assert project.id == updated_project.id == _PROJECT_ID != "a" * 64


def test_get_issues_of_the_project_none(app):
    project = Project.find_by_id(_EXISTING_PROJECT)

    assert project is not None
    assert project.issues == set()

    project_issues = Issue.search({"project": project.id})
    assert len(project_issues) > 0

    project_issues_from_self = project.get_issues()
    assert len(project_issues) == len(project.issues) == len(project_issues_from_self)
    assert set(project.issues) == {issue.id for issue in project_issues_from_self}


def test_get_issues_of_the_project_not_empty(app):
    project = Project.find_by_id(_EXISTING_PROJECT)
    assert project is not None
    # WHEN, store project's issues to DB
    project.get_issues()
    assert project.issues

    # Fetch issues based on stored keys in issues list on class
    issues = [issue.id for issue in Issue.get_all().values() if issue.project == project.id]
    issues_via_project = {issue.id for issue in project.get_issues()}
    assert set(issues) == set(project.issues) == set(issues_via_project)


_ISSUE_FROM_EXSTING_PROJECT = "c7b2e1bef0cfdeb959c0382a1ba63c4125e261ea245e7d86428b0244141cc34a"


def test_get_issue_of_the_project_issues_empty(app):
    project = Project.find_by_id(_EXISTING_PROJECT)
    assert project is not None

    issue = project.get_issue(_ISSUE_FROM_EXSTING_PROJECT)

    assert issue is not None
    assert issue.id == _ISSUE_FROM_EXSTING_PROJECT


def test_get_issue_of_the_project_issues_not_empty(app):
    project = Project.find_by_id(_EXISTING_PROJECT)
    assert project is not None

    # WHEN, will for sure update project.issues
    project.get_issues()
    assert project.issues

    issue = project.get_issue(_ISSUE_FROM_EXSTING_PROJECT)
    assert issue is not None
    assert issue.id == _ISSUE_FROM_EXSTING_PROJECT
    assert issue.id in project.issues


def test_required_issue_is_none(app):
    project = Project.find_by_id(_EXISTING_PROJECT)
    assert project is not None

    issue = project.get_issue("abcd" * 16)
    assert issue is None

    # WHEN, will for sure update project.issues
    project.get_issues()
    assert project.issues
    assert "abcd" * 16 not in project.issues
