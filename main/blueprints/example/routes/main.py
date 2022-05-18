from ...._flask_launchpad.src.flask_launchpad import FlaskLaunchpad
from flask import current_app
from flask import session
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    FlaskLaunchpad(current_app).create_all_models()

    print(session)

    """Example of route url"""
    return """Working..."""


@bp.route("/test", methods=["GET"])
def test():
    """Example of route url"""
    return """Working..."""
