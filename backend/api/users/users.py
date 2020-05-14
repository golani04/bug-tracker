from typing import Dict
from flask import jsonify

from backend.api import bp
from backend.api.errors import error_response
from backend.api.util import check_requested_data, check_required_keys
from backend.models.users import User


@bp.route("/users", methods=["GET"])
def get_users():
    return jsonify([user.to_dict() for user in User.get_all().values()]), 200


@bp.route("/users", methods=["POST"])
@check_requested_data
@check_required_keys({"name", "username", "email", "password", "project"})
def create_user(data: Dict):
    user = User.create(data)
    if user.save("create") is False:
        return error_response(500)

    return jsonify(user.to_dict()), 201

        return error_response(500)

    return jsonify(project.to_dict()), 201
