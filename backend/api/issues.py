from typing import List, Tuple
from urllib.parse import urljoin

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.issues import Issue as IssueTable
from backend.schemas.issues import Issue as IssueSchema
from backend.schemas.issues import IssueCreate


router = APIRouter()


@router.get("/", response_model=List[IssueSchema])
def get_issues(session: Session = Depends(get_db)):
    issues: List[Tuple[IssueTable]] = session.execute(select(IssueTable)).all()
    return [issue for (issue,) in issues]


@router.post("/")
async def create_issue(request: Request, session: Session = Depends(get_db)):
    data = await request.form()
    issue: IssueTable = IssueTable(**IssueCreate(**data).dict())
    session.add(issue)
    session.commit()

    return RedirectResponse(
        urljoin(str(request.base_url), "issues"), status_code=status.HTTP_303_SEE_OTHER
    )
