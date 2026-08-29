from typing import List

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.issues import Issue as IssueTable
from backend.schemas.issues import Issue as IssueSchema
from backend.schemas.users import User as UserSchema
from backend.utils.auth import auth_manager
from backend.utils.html import templates


router = APIRouter()


def get_issues_data(issues: List[IssueTable], item_id: int):
    data = [
        {
            **IssueSchema.model_validate(item).model_dump(),
            "user": UserSchema.model_validate(item.reporter).model_dump(),
        }
        for item in issues
    ]

    return data, next((issue for issue in data if issue["id"] == item_id), {})


@router.get("/")
@router.get("/{template}")
def index(
    request: Request,
    template: str | None = None,
    item_id: int = Query(None),
    session: Session = Depends(get_db),
    current_user: UserSchema = Depends(auth_manager.get_current_user),
):
    if template is None:
        return templates.TemplateResponse(request, "index.html", {"current_item": {}})

    data: List[IssueTable] = []
    current_item = {}
    if template.startswith("issues"):
        data = session.execute(select(IssueTable)).scalars().all()
        data, current_item = get_issues_data(data, item_id)
    elif template.startswith("user"):
        current_item = current_user.model_dump()

    template = template if template.endswith(".html") else f"{template}.html"
    return templates.TemplateResponse(
        request, f"pages/{template}", {"data": data, "current_item": current_item}
    )
