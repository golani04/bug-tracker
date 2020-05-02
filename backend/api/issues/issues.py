from typing import Dict
from flask import jsonify

from backend.api import bp
from backend.api.errors import error_response
from backend.api.util import (
    check_item_exists,
    check_requested_data,
    check_required_keys,
)

from backend.models.issues import Issue


@bp.route("/issues", methods=["GET"])
def get_issues():
    return jsonify([issue.to_dict() for issue in Issue.get_all().values()]), 200


@bp.route("/issues", methods=["POST"])
@check_requested_data
@check_required_keys(Issue.required_props)
def create_issue(data: Dict):
    issue = Issue.create(data)
    if issue.save("create") is False:
        return error_response(500)

    return jsonify(issue.to_dict()), 201


@bp.route("/issues/<string:item_id>", methods=["GET"])
@check_item_exists(Issue, "Required issue is missing")
def get_issue(issue: Issue):
    return jsonify(issue.to_dict()), 200
