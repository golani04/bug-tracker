from backend.config import settings
from backend.db import SessionLocal, engine
from backend.enums import Priority, Status
from backend.models.base import Base
from backend.models.issues import Issue
from backend.models.projects import Project
from backend.models.users import User


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        admin = User.create_user(email=settings.admin_email, password=settings.admin_pass)
        session.add(admin)
        session.flush()

        project = Project(name="Default", owner_id=admin.id)
        session.add(project)
        session.flush()

        session.add_all(
            [
                Issue(
                    title="Set authentication",
                    description="Create login/register forms",
                    priority=Priority.high,
                    status=Status.open,
                    reporter_id=admin.id,
                    project_id=project.id,
                ),
                Issue(
                    title="Create issue form",
                    description="Use jinja partial form",
                    priority=Priority.low,
                    status=Status.open,
                    reporter_id=admin.id,
                    project_id=project.id,
                ),
            ]
        )
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
