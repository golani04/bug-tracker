from datetime import date, datetime
from freezegun import freeze_time

from backend.models.projects import Project


@freeze_time("2020-01-01 12:01:01.123456")
def test_project():
    # should provide create and update
    # set _updated for some reason freezegun didn't work on datetime.utcnow
    project = Project("1", "test", "anyone", "Testing a project", _updated=datetime.utcnow())

    assert project._created == date.today() == date(2020, 1, 1)
    assert project._updated == datetime(2020, 1, 1, 12, 1, 1, 123456)
    assert project.id == "1"
    assert project.favorite is False  # default
