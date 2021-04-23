import logging
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.issues import Issue as IssueTable
from backend.schemas.issues import Issue as IssueSchema
from backend.schemas.projects import Project as ProjectSchema
from backend.schemas.users import User as UserSchema
from backend.utils.html import templates


router = APIRouter()
logger = logging.getLogger("bug_tracker")


@router.get("/")
@router.get("/{template}")
def index(
    request: Request,
    template: str = None,
    item_id: int = Query(None),
    session: Session = Depends(get_db),
):
    if template is None:
        return templates.TemplateResponse("index.html", {"request": request, "current_issue": {}})

    data = []
    current_issue = {}
    if template.startswith("issues"):
        data: List[IssueTable] = session.query(IssueTable).all()
        data = [
            {
                **IssueSchema.from_orm(item).dict(),
                "project": ProjectSchema.from_orm(item.project),
                "user": UserSchema.from_orm(item.owner),
            }
            for item in data
        ]
        if item_id is not None:
            current_issue = next((issue for issue in data if issue["id"] == item_id), {})

    template = template if template.endswith(".html") else f"{template}.html"
    return templates.TemplateResponse(
        f"pages/{template}", {"request": request, "data": data, "current_issue": current_issue}
    )
