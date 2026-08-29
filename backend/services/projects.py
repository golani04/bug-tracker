from pydantic import TypeAdapter

from backend.models.projects import Project as ProjectModel
from backend.repositories.projects import ProjectRepository
from backend.schemas.projects import Project as ProjectSchema, ProjectCreate


type_adapter = TypeAdapter(list[ProjectSchema])


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    def get_projects(self, owner_id: int) -> list[ProjectSchema]:
        projects = self.repository.get_by_owner(owner_id)

        return type_adapter.validate_python(projects)

    def create_project(self, data: ProjectCreate, owner_id: int) -> ProjectModel:
        project = ProjectModel(name=data.name, owner_id=owner_id)
        self.repository.create(project)

        return project

    def ensure_owner(self, project_id: int, owner_id: int) -> ProjectModel:
        project = self.repository.get_by_id(project_id)
        if project is None or project.owner_id != owner_id:
            raise ValueError("Project not found")

        return project
