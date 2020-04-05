from dataclasses import asdict, fields, is_dataclass

from backend.models.issues import Issue, Severity

_ISSUE_ID = "567890abcdefghijklmnopqrstuvwxyz" * 2
_PROJECT_ID = "123456abcdefghijklmnopqrstuvwxyz" * 2
_MAINTAINER_ID = "123456abcdefghijklmnopqrstuvwxyz"[::-1] * 2


def test_issue_model():
    issue = Issue(
        _ISSUE_ID, "Lorem ipsum dolor", _MAINTAINER_ID, _MAINTAINER_ID, _PROJECT_ID
    )

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
