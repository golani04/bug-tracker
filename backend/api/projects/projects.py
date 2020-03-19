from typing import Dict
from flask import jsonify

from backend.api import bp
from backend.api.util import check_requested_data, check_required_keys, check_item_exists

from backend.models.projects import Project


@bp.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(Project.get_all_projects()), 200


@bp.route("/projects", methods=["POST"])
@check_requested_data
@check_required_keys({"name", "maintainer"})
def create_project(data: Dict):
    project = Project.create(**data)
    project.save()

    return jsonify(project.to_dict()), 201


@bp.route("/projects/<string:project_id>", methods=["GET"])
@check_item_exists(Project, "Required project is missing")
def get_project(project: Project):
    return jsonify(project.to_dict()), 200


@bp.route("/projects/<string:project_id>", methods=["PUT", "PATCH"])
@check_requested_data
@check_item_exists(Project, "Required project is missing")
def update_project(project: Project):
    return jsonify(), 200


@bp.route("/projects/<string:project_id>", methods=["DELETE"])
@check_item_exists(Project, "Required project is missing")
def delete_project(project: Project):
    return jsonify(), 200
