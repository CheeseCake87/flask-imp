import flask
from flask import current_app
from flask import session

from ...._flask_launchpad.src.flask_launchpad import FlaskLaunchpad
from ...._flask_launchpad.src.flask_launchpad import Security

from .. import bp

security = Security(current_app)


@bp.route("/", methods=["GET"])
def index():
    print(session)
    return """
index route in example Blueprint
    """


@bp.route("/account-fail", methods=["GET"])
@security.login_required("exmaple_blueprint.not_logged_in", "not_logged_in")
def account_dashboard_fail():
    return """
This should redirect to not_logged_in if you are not logged in.
    """


@bp.route("/login-redirect", methods=["GET"])
@security.no_login_required("exmaple_blueprint.already_logged_in", "logged_in")
def login_redirect():
    return """
This should redirect to already_logged_in if you are already logged in.
    """


@bp.route("/permission-redirect", methods=["GET"])
@security.permission_required("exmaple_blueprint.permission_needed", "permissions", "that")
def permission_redirect():
    return """
You have the required permission to view this page.
    """


@bp.route("/create-all-models", methods=["GET"])
def create_all_models():
    """
    Example of flask_launchpads ability to create all models
    """
    FlaskLaunchpad(current_app).create_all_models()
    return """If you didn't see an error, this probably worked..."""


@bp.route("/not-logged-in", methods=["GET"])
def not_logged_in():
    print(flask.get_flashed_messages())
    return """error - see terminal"""


@bp.route("/already-logged-in", methods=["GET"])
def already_logged_in():
    print(flask.get_flashed_messages())
    return """error - see terminal"""


@bp.route("/permission-needed", methods=["GET"])
def permission_needed():
    print(flask.get_flashed_messages())
    return """error - see terminal"""


@bp.route("/example-structure", methods=["GET"])
def test():
    return """test route in example Blueprint"""
