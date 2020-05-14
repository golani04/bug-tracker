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


@bp.route("/users/<string:item_id>", methods=["GET"])
@check_item_exists(User, "Required user is missing")
def get_user(user: User):
    return jsonify(user.to_dict()), 200


@bp.route("/users/<string:item_id>", methods=["PATCH"])
@check_requested_data
@filter_unchangeable_keys(User.unchangeable_props)
@check_item_exists(User, "Required user is missing")
def update_user(user: User, data: Dict):
    user = user.modify(data)
    if user.save("modify") is False:
        return error_response(500)
    return jsonify(user.to_dict()), 200
