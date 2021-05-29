import logging
from datetime import date, datetime

from sqlalchemy.orm import Session

from backend.models.issues import Issue
from backend.models.users import User
from backend.schemas.issues import Issue as IssueSchema
from backend.schemas.issues import Label, Severity, Status
from backend.schemas.users import User as UserSchema
from backend.utils.auth import hash_password


logger = logging.getLogger("bug_tracker")


def test_engine(session: Session):
    engine = session.connection().engine

    assert str(engine.url) == "sqlite+pysqlite:///:memory:"


_SOME_ISSUE = {
    "title": "Testing Model",
    "type": "Issue model testing",
    "description": "Testing",
    "severity": int(Severity.high),
    "status": int(Status.completed),
    "label": int(Label.enhancement),
    "due": date.today(),
    "reporter": 1,
}


def test_issue_model(session: Session):
    issue = Issue(**_SOME_ISSUE)
    session.add(issue)
    session.flush()

    assert issue.active is True
    assert isinstance(issue.created_at, datetime)
    assert all(v == _SOME_ISSUE[k] for k, v in IssueSchema.from_orm(issue) if k in _SOME_ISSUE)


_SOME_USER = {
    "firstname": "Test",
    "lastname": "Tester",
    "username": "tester",
    "email": "tester@example.com",
    "password": hash_password("password"),
}


def test_user_model(session: Session):
    user = User(**_SOME_USER)
    session.add(user)
    session.flush()

    assert user.active is True
    assert isinstance(user.created_at, datetime)
    assert all(v == _SOME_USER[k] for k, v in UserSchema.from_orm(user) if k in _SOME_USER)


def test_user_and_issues(session: Session):
    user = User(**_SOME_USER)
    issue = Issue(**_SOME_ISSUE)

    session.add_all([user, issue])
    session.commit()

    assert issue.owner == user
    assert user.issues == [issue]
