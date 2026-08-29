from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.logger import logger
from backend.repositories.issues import IssueRepository
from backend.schemas.common import IdResponse
from backend.schemas.issues import Issue as IssueSchema, IssueUpdate
from backend.schemas.users import User as UserSchema
from backend.services.issues import IssueService
from backend.utils.auth import auth_manager


router = APIRouter()


@router.get("/{issue_id}", response_model=IssueSchema, status_code=status.HTTP_200_OK)
async def get_issue(
    issue_id: int,
    current_user: UserSchema = Depends(auth_manager.get_current_user),
    session: Session = Depends(get_db),
):
    service = IssueService(IssueRepository(session))
    try:
        return service.get_issue(issue_id, current_user.id)
    except ValueError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Issue not found") from error


@router.patch("/{issue_id}", response_model=IdResponse, status_code=status.HTTP_200_OK)
async def update_issue(
    issue_id: int,
    data: IssueUpdate,
    current_user: UserSchema = Depends(auth_manager.get_current_user),
    session: Session = Depends(get_db),
):
    service = IssueService(IssueRepository(session, filters={"id": issue_id, "active": True}))
    try:
        service.get_issue(issue_id, current_user.id)
    except ValueError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Issue not found") from error

    try:
        updated_id = service.update_issue(data)
    except ValueError as error:
        logger.error(f"Failed to update issue {issue_id}. Error {error}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Update failed.") from error

    return IdResponse(id=updated_id)
