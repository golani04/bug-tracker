from flask import jsonify

from backend import db
from backend.api import bp


@bp.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(Project.get_all_projects()), 200


@bp.route("/projects", methods=["POST"])
def create_project():
    return jsonify(), 201


@bp.route("/projects/<string:project_id>", methods=["GET"])
def get_project(project_id: str):
    return jsonify(), 200


@bp.route("/projects/<string:project_id>", methods=["PUT", "PATCH"])
def update_project(project_id: str):
    return jsonify(), 200


@bp.route("/projects/<string:project_id>", methods=["DELETE"])
def delete_project(project_id: str):
    return jsonify(), 200
