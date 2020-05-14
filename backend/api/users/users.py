from flask import jsonify

from backend.api import bp
from backend.models.users import User


@bp.route("/users", methods=["GET"])
def get_users():
    return jsonify([user.to_dict() for user in User.get_all().values()]), 200
