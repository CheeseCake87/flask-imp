from ...._flask_launchpad.src.flask_launchpad import FlaskLaunchpad
from flask import current_app
from flask import session
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return """Working..."""


@bp.route("/create-all-models", methods=["GET"])
def create_all_models():
    """
    Example of flask_launchpads ability to create all models
    """
    FlaskLaunchpad(current_app).create_all_models()
    return """Working..."""


@bp.route("/test", methods=["GET"])
def flask_config_output():
    """
    Example of route url
    """
    return """Working..."""
