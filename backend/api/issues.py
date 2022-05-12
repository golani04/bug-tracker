import logging
from typing import List, Tuple
from urllib.parse import urljoin

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.issues import Issue as IssueTable
from backend.schemas.issues import Issue as IssueSchema, IssueCreate, IssueUpdate


router = APIRouter()
logger = logging.getLogger("bug_tracker")


@router.get("/", response_model=List[IssueSchema])
def get_issues(session: Session = Depends(get_db)):
    issues: List[Tuple[IssueTable]] = session.execute(select(IssueTable)).all()
    return [IssueSchema.from_orm(issue).dict() for (issue,) in issues]


@router.post("/")
async def create_issue(request: Request, session: Session = Depends(get_db)):
    data = await request.form()

    issue: IssueTable = IssueTable(**IssueCreate(**data).dict())
    session.add(issue)
    session.commit()

    return RedirectResponse(
        urljoin(str(request.base_url), "issues"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.put("/{issue_id}")
@router.post("/{issue_id}")
async def update_issue(issue_id: int, request: Request, session: Session = Depends(get_db)):
    data = await request.form()
    logger.info(data)

    logger.info(IssueUpdate(**data).dict(exclude_unset=True))
    results: int = (
        session.query(IssueTable)
        .filter(IssueTable.id == issue_id)
        .update(IssueUpdate(**data).dict(exclude_unset=True))
    )

    session.commit()

    if not results:
        logger.warning(f"Issue #{issue_id} has not been updated.")

    return RedirectResponse(
        urljoin(str(request.base_url), "issues"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.delete("/{issue_id}")
@router.post("/{issue_id}/delete")
async def delete_issue(issue_id: int, request: Request, session: Session = Depends(get_db)):
    issue: IssueTable = session.query(IssueTable).filter_by(id=issue_id).first()

    issue.delete()  # soft delete
    session.commit()

    return RedirectResponse(
        urljoin(str(request.base_url), "issues"), status_code=status.HTTP_303_SEE_OTHER
    )
