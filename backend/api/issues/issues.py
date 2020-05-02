from typing import Dict
from flask import jsonify

from backend.api import bp

from backend.models.issues import Issue


@bp.route("/issues", methods=["GET"])
def get_issues():
    return jsonify([issue.to_dict() for issue in Issue.get_all().values()]), 200
