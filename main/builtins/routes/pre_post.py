from flask import current_app
from flask import session


@current_app.before_first_request
def before_first_request():
    pass


@current_app.before_request
def before_request():
    if "version" not in session:
        session["version"] = current_app.config["VERSION"]
    if "error" not in session:
        session["error"] = None
    if "message" not in session:
        session["message"] = None


@current_app.after_request
def after_request(response):
    return response
