from backend.db import Base, engine, get_db
from backend.models import issues, users
from backend.schemas.issues import Label, Severity, Status

from config import settings

# init database
Base.metadata.create_all(bind=engine)


session = next(get_db())


session.add(
    users.User.create_user(
        **dict(
            email=settings.admin_email,
            username=settings.admin_user,
            password=settings.admin_pass,
            firstname="Leonid",
            lastname="Spivak",
        ),
    )
)

session.add_all(
    [
        issues.Issue(
            title="Set authentication",
            description="Create login/register forms",
            severity=Severity.high,
            status=Status.opened,
            label=Label.enhancement,
            reporter=1,
        ),
        issues.Issue(
            title="Create issue form",
            description="Use jinja partial form",
            severity=Severity.low,
            status=Status.opened,
            label=Label.enhancement,
            reporter=1,
        ),
    ]
)
session.commit()
