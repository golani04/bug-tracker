from datetime import date

from starlette.templating import Jinja2Templates

from backend.enums import Priority, Status


templates = Jinja2Templates(directory="frontend/components")
templates.env.globals = {
    **templates.env.globals,
    "priority": Priority,
    "status": Status,
    "current_year": date.today().year,
    "current_date": date.today(),
}
