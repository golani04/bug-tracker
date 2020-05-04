from dataclasses import asdict, fields, is_dataclass
from datetime import date, timedelta
from freezegun import freeze_time

import pytest
from backend.models.issues import Issue, Status, Severity

_ISSUE_ID = "567890abcdefghijklmnopqrstuvwxyz" * 2
_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2
# in demo data issues randomly taken from the list
_EXISTING_ISSUE_ID = "a1c728c5e9680804ea35b234e04b60e91aad32d375b3a1cbb6b035be69221a1e"


def test_issue_model():
    issue = Issue(_ISSUE_ID, "Lorem ipsum dolor", _MAINTAINER_ID, _MAINTAINER_ID, _PROJECT_ID)

    assert is_dataclass(issue)
    # test random enum object
    assert issue.severity == Severity.low


def test_get_all_issues(app):
    issues = Issue.get_all()
    assert len(issues) == 30

    issues_0 = asdict(list(issues.values())[0])
    assert set(issues_0.keys()) <= {prop.name for prop in fields(Issue)}


def test_issue_to_dict_method(app):
    issue = list(Issue.get_all().values())[0]
    issue_dict = issue.to_dict()

    assert issue.id == issue_dict["id"]
    assert issue.severity.value == issue_dict["severity"]


def test_find_by_id(app):
    issue = Issue.find_by_id(_EXISTING_ISSUE_ID)

    assert issue is not None
    assert is_dataclass(issue)
    assert issue.id == _EXISTING_ISSUE_ID


def test_find_by_id_that_not_exist(app):
    # _ISSUE_ID is not exising id that used for tests
    issue = Issue.find_by_id(_ISSUE_ID)

    assert issue is None


def test_issue_delete_without_save_missing_in_db(app):
    # given
    issue = Issue.find_by_id(_EXISTING_ISSUE_ID)
    # when #
    issue.delete()
    # then
    assert Issue.get_all().get(issue.id) is None
    # when, check that DB did not changed
    Issue.get_all.cache_clear()
    # then
    assert Issue.get_all().get(issue.id) == issue


@freeze_time("2020-01-01")
def test_issue_create(app):
    issue = Issue.create(
        {
            "title": "Test createIssue",
            "description": "Created test issue.",
            "assignee": _MAINTAINER_ID,
            "reporter": _MAINTAINER_ID,
            "project": _PROJECT_ID,
            "links": "https://www.google.com/search?q=testings",
            "severity": 1,
            "status": 4,
            "time_spent": {"days": 1, "hours": 11},
        }
    )

    assert issue is not None
    assert issue.assignee == _MAINTAINER_ID
    assert issue.created == date(2020, 1, 1)
    assert issue.time_spent == timedelta(**{"days": 1, "hours": 11}).total_seconds()

    _ID = issue.id
    assert Issue.find_by_id(_ID) is None

    issue.save("create")
    assert Issue.find_by_id(_ID) is not None


def test_issue_delete(app):
    # given
    issue = Issue.find_by_id(_EXISTING_ISSUE_ID)
    assert issue is not None
    # when
    issue.delete()
    # when, call save method to register it to DB
    issue.save("delete")
    # then
    assert Issue.get_all().get(issue.id) is None


def test_issue_delete_none(app):
    issue = Issue.find_by_id(_ISSUE_ID)
    assert issue is None


def test_issue_modify(app):
    # given
    issue = Issue.find_by_id(_EXISTING_ISSUE_ID)
    assert issue is not None
    # when
    data = {
        "title": "Issue 111",
        "description": "Integer ac leo. Pellentesque ultrices mattis odio.",
        "assignee": _MAINTAINER_ID,
        "links": "https://www.google.com/search?q=testings",
        "severity": 1,
        "status": 4,
    }
    issue = issue.modify(data)
    # then
    assert issue.id == _EXISTING_ISSUE_ID
    assert issue.assignee == _MAINTAINER_ID
    assert issue.title == data["title"]
    assert issue.links == data["links"]
    assert issue.severity == Severity.low
    assert issue.status == Status.close


def test_issue_modify_unchangeable_keys(app):
    # given
    issue = Issue.find_by_id(_EXISTING_ISSUE_ID)
    assert issue is not None
    # when
    data = {
        "id": _ISSUE_ID,
        "reporter": _MAINTAINER_ID,
        "project": _PROJECT_ID,
        "created": "2020-04-29",
    }
    issue = issue.modify(data)
    # then
    assert issue.id != _ISSUE_ID
    assert issue.reporter != _MAINTAINER_ID
    assert issue.project != _PROJECT_ID
    assert issue.created != data["created"]


def test_issue_modify_saved(app):
    # given
    issue = Issue.find_by_id(_EXISTING_ISSUE_ID)
    assert issue is not None

    # when
    issue = issue.modify({"title": "Issue 111"})
    # then
    assert issue.title == "Issue 111"

    # when, not saved
    Issue.get_all.cache_clear()
    issue = Issue.find_by_id(_EXISTING_ISSUE_ID)
    # then
    assert issue.title != "Issue 111"

    # when, saved
    issue = issue.modify({"title": "Issue 111"})
    issue.save("modify")
    Issue.get_all.cache_clear()
    issue = Issue.find_by_id(_EXISTING_ISSUE_ID)
    # then
    assert issue.title == "Issue 111"


@pytest.mark.parametrize(
    "props,expected",
    [
        ({"status": 3}, 7),
        ({"status": 3, "severity": 1}, 5),
        (
            {
                "project": "218116e27cd7ffb160028c8e9c661ce6f880a69419239d524118244082fdafdb",
                "severity": 3,
            },
            4,
        ),
        (
            {
                "reporter": "f1120082590e21a79396b79cbb1995c4f5f090171dcad05ac899cb1d6ed8905b",
                "project": "c0e898915bd4f2c0fed3cf657609ce2e5ea885d2fbcf923393352962488b008c",
            },
            1,
        ),
    ],
)
def test_search_issues_values_eq(props, expected, app):
    assert len(Issue.search(props)) == expected


@pytest.mark.parametrize(
    "props,expected",
    [
        (
            {"id": "6c7ce96a6d7502e89b93d54744389f800d0ab317cffc75caf7e0815c56fae438", "status": 3},
            7,
        ),
        ({"status": 3, "severity": 1, "title": "Lorem ipsum"}, 5),
    ],
)
def test_search_issues_values_eq_unsearch_props(props, expected, app):
    assert len(Issue.search(props)) == expected


def test_search_issues_values_eq_fails(app):
    assert Issue.search({"status": 5, "severity": 0}) == []
