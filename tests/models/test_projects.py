import pytest
from datetime import date, datetime
from freezegun import freeze_time

from backend.models.projects import Project
from backend.models.validate import ValidationError


_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2


@freeze_time("2020-01-01 12:01:01.123456")
def test_project():
    # GIVEN
    # should provide create and update
    project = Project(_PROJECT_ID, "test", _MAINTAINER_ID, "Testing a project")
    # WHEN
    # set _updated for some reason freezegun didn't work on datetime.utcnow
    project._updated = datetime.utcnow()
    # THEN
    assert project._created == date.today() == date(2020, 1, 1)
    assert project._updated == datetime(2020, 1, 1, 12, 1, 1, 123456)
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
