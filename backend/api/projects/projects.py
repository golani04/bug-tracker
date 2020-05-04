from typing import Dict
from flask import jsonify

from backend.api import bp
from backend.api.errors import error_response
from backend.api.util import (
    check_requested_data,
    check_required_keys,
    check_item_exists,
    filter_unchangeable_keys,
)

from backend.models.projects import Project


@bp.route("/projects", methods=["GET"])
def get_projects():
    return jsonify([project.to_dict() for project in Project.get_all().values()]), 200


@bp.route("/projects", methods=["POST"])
@check_requested_data
@check_required_keys({"name", "maintainer"})
def create_project(data: Dict):
    project = Project.create(**data)
    if project.save("create") is False:
        return error_response(500)

    return jsonify(project.to_dict()), 201


@bp.route("/projects/<string:item_id>", methods=["GET"])
@check_item_exists(Project, "Required project is missing")
def get_project(project: Project):
    return jsonify(project.to_dict()), 200


@bp.route("/projects/<string:item_id>/issues", methods=["GET"])
@check_item_exists(Project, "Required project is missing")
def get_project_issues(project: Project):
    return jsonify([issue.to_dict() for issue in project.get_issues()]), 200


@bp.route("/projects/<string:item_id>", methods=["PATCH"])
@check_requested_data
@filter_unchangeable_keys(Project.unchangeable_props)
@check_item_exists(Project, "Required project is missing")
def update_project(project: Project, data: Dict):
    project = project.modify(data)
    if project.save("modify") is False:
        return error_response(500)

    return jsonify(project.to_dict()), 200


@bp.route("/projects/<string:item_id>", methods=["DELETE"])
@check_item_exists(Project, "Required project is missing")
def delete_project(project: Project):
    project.delete()
    if project.save("delete") is False:
        return error_response(500)

    return jsonify(), 204
