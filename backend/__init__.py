from flask import Flask

# blueprints
from backend.main import bp as main_bp
from backend.api import bp as api_bp


def create_app():
    app = Flask(__name__)

    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v0/")
