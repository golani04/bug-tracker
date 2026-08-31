from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.repositories.issues import IssueRepository
from backend.repositories.projects import ProjectRepository
from backend.schemas.common import IdResponse
from backend.schemas.issues import Issue as IssueSchema, IssueArgs, IssueCreate
from backend.schemas.projects import Project as ProjectSchema, ProjectCreate
from backend.schemas.users import User as UserSchema
from backend.services.issues import IssueService
from backend.services.projects import ProjectService
from backend.utils.auth import auth_manager


router = APIRouter()


@router.get("", response_model=list[ProjectSchema], status_code=status.HTTP_200_OK)
async def list_projects(
    current_user: UserSchema = Depends(auth_manager.get_current_user),
    session: Session = Depends(get_db),
):
    service = ProjectService(ProjectRepository(session))
    return service.get_projects(current_user.id)


@router.post("", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    current_user: UserSchema = Depends(auth_manager.get_current_user),
    session: Session = Depends(get_db),
):
    service = ProjectService(ProjectRepository(session))
    return service.create_project(data, owner_id=current_user.id)


@router.get("/{project_id}/issues", response_model=list[IssueSchema], status_code=status.HTTP_200_OK)
async def list_project_issues(
    project_id: int,
    query_params: IssueArgs = Depends(),
    current_user: UserSchema = Depends(auth_manager.get_current_user),
    session: Session = Depends(get_db),
):
    project_service = ProjectService(ProjectRepository(session))
    try:
        project_service.ensure_owner(project_id, current_user.id)
    except ValueError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Project not found") from error

    issue_service = IssueService(IssueRepository(session))
    return issue_service.get_issues(query_params, project_id=project_id)


@router.post(
    "/{project_id}/issues", response_model=IdResponse, status_code=status.HTTP_201_CREATED
)
async def create_project_issue(
    project_id: int,
    data: IssueCreate,
    current_user: UserSchema = Depends(auth_manager.get_current_user),
    session: Session = Depends(get_db),
):
    project_service = ProjectService(ProjectRepository(session))
    try:
        project_service.ensure_owner(project_id, current_user.id)
    except ValueError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Project not found") from error

    issue_service = IssueService(IssueRepository(session))
    try:
        issue_id = issue_service.create_issue(
            data, reporter_id=current_user.id, project_id=project_id
        )
    except ValueError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Failed to create issue.") from error

    return IdResponse(id=issue_id)
