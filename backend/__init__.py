from flask import Flask

from backend.db import DB
from backend.config import db_config

# blueprints
from backend.main import bp as main_bp

database = DB()


def create_app(db_config: object = db_config):
    app = Flask(__name__)
    database.config = db_config

    register_blueprints(app)
    return app


def register_blueprints(app):
    # prevent circular imports
    from backend.api import bp as api_bp  # noqa

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v0/")
