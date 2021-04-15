from backend.schemas.issues import Label, Severity, Status
from backend.db import Base, engine, get_db
from backend.models import projects, users, issues
from backend.schemas.users import UserType
from config import settings


# init database
Base.metadata.create_all(bind=engine)


session = next(get_db())


session.add(
    users.User.create_user(
        settings.admin_email,
        settings.admin_user,
        settings.admin_pass,
        "Admin",
        "Admin",
        int(UserType.admin),
    )
)
session.add(projects.Project.create("Bug tracker", 1))
session.add_all(
    [
        issues.Issue(
            title="Set authentication",
            description="Create login/register forms",
            severity=Severity.high,
            status=Status.opened,
            label=Label.enhancement,
            reporter=1,
            project_id=1,
        ),
        issues.Issue(
            title="Create issue form",
            description="Use jinja partial form",
            severity=Severity.low,
            status=Status.opened,
            label=Label.enhancement,
            reporter=1,
            project_id=1,
        ),
    ]
)
session.commit()
