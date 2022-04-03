from ....builtins.functions.security import login_required
from flask import url_for
from flask import request
from flask import session
from flask import abort
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return f"""example route"""


@bp.route("/this-page-is-locked", methods=["GET"])
def page_is_locked():
    return f"""This page is locked"""


@bp.route("/locked-page", methods=["GET"])
@login_required(on_error_endpoint="nothere")
def locked_page():
    return f"""On the locked page"""


@bp.route("/admin", methods=["GET"])
def admin():
    return f"""administrator section"""


@bp.route("/login", methods=["GET"])
def login():
    if request.method == "POST":
        if session["form_token"] != request.form["form_token"]:
            abort(404)
    return f"""administrator section"""


@bp.route("/logout", methods=["GET"])
def logout():
    return f"""administrator section"""


@bp.route("/reset-password", methods=["GET"])
def reset_password():
    return f"""administrator section"""
