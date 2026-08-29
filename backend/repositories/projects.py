from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.projects import Project as ProjectModel


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session
        self.table = ProjectModel

    def get_by_id(self, project_id: int) -> ProjectModel | None:
        statement = select(self.table).where(self.table.id == project_id, self.table.active.is_(True))
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_owner(self, owner_id: int) -> Sequence[ProjectModel]:
        statement = select(self.table).where(
            self.table.owner_id == owner_id, self.table.active.is_(True)
        )
        return self.session.execute(statement).scalars().fetchall()

    def create(self, project: ProjectModel) -> int:
        self.session.add(project)
        self.session.flush()

        return project.id
