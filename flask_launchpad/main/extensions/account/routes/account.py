from flask_launchpad.main.builtins.functions.security import login_required
from .. import bp
from .. import Structure
from .. import extmod
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for


@bp.route("/", methods=["GET"])
@login_required(session_bool_key="auth", on_error_endpoint="example1.login")
def account():
    """
    This page is protected by the login_required decorator, with the login page endpoint set.
    """
    return f"""Account Page {session}"""
