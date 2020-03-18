from flask import Blueprint

bp = Blueprint("api", __name__)


@bp.before_request
def _before_req():
    """Load current user"""


@bp.after_request
def _after_req(response):
    """Update user activity timeout."""

    return response


from .projects import projects  # noqa
