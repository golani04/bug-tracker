from urllib.parse import urljoin

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import update
from sqlalchemy.orm import session

from backend.db import get_db
from backend.models.users import User as UserTable
from backend.schemas.users import UserUpdate


router = APIRouter()


@router.post("/{user_id}")
async def get_issue(request: Request, user_id: int, session: session = Depends(get_db)):
    data = await request.form()
    session.execute(
        update(UserTable)
        .where(UserTable.id == user_id)
        .values(**UserUpdate(**data).dict(exclude_unset=True))
    )
    session.commit()

    return RedirectResponse(
        urljoin(str(request.base_url), "user"), status_code=status.HTTP_303_SEE_OTHER
    )
