import flask
from flask import current_app
from app import security

from ...._flask_launchpad.src.flask_launchpad import FlaskLaunchpad
from .. import bp


@bp.route("/account-fail", methods=["GET"])
@security.login_required("exmaple_blueprint.not_logged_in", "not_logged_in")
def account_dashboard_fail():
    """
    Login required route, sends user to url_for example.not_logged_in if session var not_logged_in is false
    """
    return "This should redirect to not_logged_in if you are not logged in."


#
@bp.route("/login-redirect", methods=["GET"])
@security.no_login_required("exmaple_blueprint.already_logged_in", "logged_in")
def login_redirect():
    """
    No login required, this redirects the user to example_blueprint.already_logged_in if the session var logged_in is true
    """
    return "This should redirect to already_logged_in if you are already logged in."


@bp.route("/permission-redirect", methods=["GET"])
@security.permission_required("exmaple_blueprint.permission_needed", "permissions", "that")
def permission_redirect():
    """
    This redirects the user to example_blueprint.permission_needed if the required permission is not found
    permission_required(endpoint, key in session(session[key]), value in the list of key)
    session['permissions] = ['this', 'that', 'here', 'there']
    """
    return "You have the required permission to view this page."


@bp.route("/create-all-models", methods=["GET"])
def create_all_models():
    """
    Example of flask_launchpads ability to create all models
    """
    FlaskLaunchpad(current_app).create_all_models()
    return """If you didn't see an error, this probably worked..."""


@bp.route("/not-logged-in", methods=["GET"])
def not_logged_in():
    message = flask.get_flashed_messages()
    return f"{message}"


@bp.route("/already-logged-in", methods=["GET"])
def already_logged_in():
    message = flask.get_flashed_messages()
    return f"{message}"


@bp.route("/permission-needed", methods=["GET"])
def permission_needed():
    message = flask.get_flashed_messages()
    return f"{message}"
