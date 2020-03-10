from flask import jsonify, request

from backend.api import bp
from backend.api.errors import bad_request

from backend.models.projects import Project


@bp.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(Project.get_all_projects()), 200


@bp.route("/projects", methods=["POST"])
def create_project():
    data = request.get_json()
    if data is None:
        return bad_request("Missing payload or payload is not json.")

    project = Project.create(**data)
    project.save()

    return jsonify(project), 201


@bp.route("/projects/<string:project_id>", methods=["GET"])
def get_project(project_id: str):
    return jsonify(), 200


@bp.route("/projects/<string:project_id>", methods=["PUT", "PATCH"])
def update_project(project_id: str):
    return jsonify(), 200


@bp.route("/projects/<string:project_id>", methods=["DELETE"])
def delete_project(project_id: str):
    return jsonify(), 200
