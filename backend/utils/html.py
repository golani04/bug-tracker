from datetime import date

from starlette.templating import Jinja2Templates

from backend.schemas.issues import Label, Severity, Status


templates = Jinja2Templates(directory="frontend/components")
templates.env.globals = {
    **templates.env.globals,
    "severity": Severity,
    "status": Status,
    "label": Label,
    "current_year": date.today().year,
    "current_date": date.today(),
}
