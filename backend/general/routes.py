import logging
from typing import List

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.issues import Issue as IssueTable
from backend.schemas.issues import Issue as IssueSchema
from backend.schemas.users import User as UserSchema
from backend.utils.auth import auth_manager
from backend.utils.html import templates


router = APIRouter()
logger = logging.getLogger("bug_tracker")


def get_issues_data(issues: List[IssueTable], item_id: int):
    data = [
        {
            **IssueSchema.from_orm(item).dict(),
            # "project": ProjectSchema.from_orm(item.project),
            "user": UserSchema.from_orm(item.owner),
        }
        for item in issues
    ]

    return data, next((issue for issue in data if issue["id"] == item_id), {})


@router.get("/")
@router.get("/{template}")
def index(
    request: Request,
    template: str = None,
    item_id: int = Query(None),
    session: Session = Depends(get_db),
    current_user=Depends(auth_manager.get_current_user),
):
    if template is None:
        return templates.TemplateResponse("index.html", {"request": request, "current_item": {}})

    data: List[IssueTable] = []
    current_item = {}
    if template.startswith("issues"):
        data = session.query(IssueTable).all()
        data, current_item = get_issues_data(data, item_id)
    elif template.startswith("user"):
        current_item = UserSchema.from_orm(current_user).dict()

    template = template if template.endswith(".html") else f"{template}.html"
    return templates.TemplateResponse(
        f"pages/{template}", {"request": request, "data": data, "current_item": current_item}
    )
