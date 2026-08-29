from backend.models.projects import Project as ProjectModel
from backend.models.users import User as UserModel
from backend.repositories.projects import ProjectRepository
from backend.repositories.users import UserRepository
from backend.schemas.users import UserCreate, UserUpdate
from backend.utils.security import hash_password, verify_password


class UserService:
    def __init__(self, repository: UserRepository, project_repository: ProjectRepository) -> None:
        self.repository = repository
        self.project_repository = project_repository

    def sign_up(self, data: UserCreate) -> UserModel:
        user = UserModel.create_user(email=data.email, password=data.password.get_secret_value())
        self.repository.create(user)

        project = ProjectModel(name="Default", owner_id=user.id)
        self.project_repository.create(project)

        return user

    def login(self, email: str, password: str) -> UserModel:
        user = self.repository.get_by_email(email)
        if user is None:
            verify_password("timingattack", hash_password("timingattack"))
            raise ValueError("Username or password are incorrect")

        if not verify_password(password, user.password_hash.encode()):
            verify_password("timingattack", hash_password("timingattack"))
            raise ValueError("Username or password are incorrect")

        return user

    def get_by_id(self, user_id: int) -> UserModel | None:
        return self.repository.get_by_id(user_id)

    def update(self, user_id: int, data: UserUpdate) -> int:
        return self.repository.update(
            user_id, data.model_dump(exclude_none=True, exclude_unset=True)
        )
