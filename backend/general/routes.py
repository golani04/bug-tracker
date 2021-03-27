import logging

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
logger = logging.getLogger("bug_tracker")
templates = Jinja2Templates(directory="frontend/components")


@router.get("/")
@router.get("/{template}")
def index(request: Request, template: str = None):
    if template is None:
        template = "index"

    return templates.TemplateResponse(f"{template}.html", {"request": request})
