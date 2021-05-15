import logging
from typing import List

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.issues import Issue as IssueTable
from backend.models.users import User as UserTable
from backend.schemas.issues import Issue as IssueSchema
from backend.schemas.users import User as UserSchema
from backend.utils.html import templates


router = APIRouter()
logger = logging.getLogger("bug_tracker")


def get_issues_data(data: List[IssueTable], item_id: int):
    data = [
        {
            **IssueSchema.from_orm(item).dict(),
            "project": ProjectSchema.from_orm(item.project),
            "user": UserSchema.from_orm(item.owner),
        }
        for item in data
    ]

    return data, next((issue for issue in data if issue["id"] == item_id), {})


@router.get("/")
@router.get("/{template}")
def index(
    request: Request,
    template: str = None,
    item_id: int = Query(None),
    session: Session = Depends(get_db),
):
    if template is None:
        return templates.TemplateResponse("index.html", {"request": request, "current_item": {}})

    data = []
    current_item = {}
    if template.startswith("issues"):
        data: List[IssueTable] = session.query(IssueTable).all()
        data, current_item = get_issues_data(data, item_id)
    elif template.startswith("user"):
        user: List[IssueTable] = session.query(UserTable).one_or_none()
        current_item = UserSchema.from_orm(user).dict()

    template = template if template.endswith(".html") else f"{template}.html"
    return templates.TemplateResponse(
        f"pages/{template}", {"request": request, "data": data, "current_item": current_item}
    )
