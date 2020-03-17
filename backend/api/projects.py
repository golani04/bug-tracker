from flask import jsonify, request

from backend.api import bp
from backend.api.errors import bad_request

from backend.models.projects import Project


@bp.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(Project.get_all_projects()), 200


# TODO: create a decorator that will check errors in received json
#       this decorator will store required keys for validation
@bp.route("/projects", methods=["POST"])
def create_project():
    data = request.get_json()
    error_msg = ""
    required_keys = {"name", "maintainer"}

    if data is None:
        error_msg = "Provided data is not a json."
    elif not data:
        error_msg = "Received json is empty."
    elif not required_keys <= set(data):
        keys = required_keys - set(data)
        error_msg = (
            f"Missing required key{'s' if len(keys) > 1 else ''}: {', '.join(sorted(keys))}."
        )

    if error_msg:
        return bad_request(error_msg)

    project = Project.create(**data)
    project.save()

    return jsonify(project.to_dict()), 201


@bp.route("/projects/<string:project_id>", methods=["GET"])
def get_project(project_id: str):
    return jsonify(), 200


@bp.route("/projects/<string:project_id>", methods=["PUT", "PATCH"])
def update_project(project_id: str):
    return jsonify(), 200


@bp.route("/projects/<string:project_id>", methods=["DELETE"])
def delete_project(project_id: str):
    return jsonify(), 200
