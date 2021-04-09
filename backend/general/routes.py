import logging

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse


router = APIRouter()
logger = logging.getLogger("bug_tracker")
templates = Jinja2Templates(directory="frontend/components")


@router.get("/")
@router.get("/{template}")
def index(request: Request, template: str = None):
    if template is None:
        return templates.TemplateResponse("index.html", {"request": request})

    template = template if template.endswith(".html") else f"{template}.html"
    return templates.TemplateResponse(f"pages/{template}", {"request": request})
