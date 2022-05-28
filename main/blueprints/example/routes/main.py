from flask import current_app

from ...._flask_launchpad.src.flask_launchpad import FlaskLaunchpad

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return """index route in example Blueprint"""


@bp.route("/create-all-models", methods=["GET"])
def create_all_models():
    """
    Example of flask_launchpads ability to create all models
    """
    FlaskLaunchpad(current_app).create_all_models()
    return """If you didn't see an error, this probably worked..."""


@bp.route("/example-structure", methods=["GET"])
def test():
    return """test route in example Blueprint"""
