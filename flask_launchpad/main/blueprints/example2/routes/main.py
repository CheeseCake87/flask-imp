from ....builtins.functions.security import login_required
from .. import bp
from flask import request
from flask import session
from flask import redirect
from flask import url_for


@bp.route("/", methods=["GET"])
def index():
    return f"""example route"""


@bp.route("/no-endpoint-login-required", methods=["GET"])
@login_required(session_bool_key="example2_auth", on_error_endpoint="nothere")
def locked_page():
    """
    Used to test the error catching ability of the system if a non-existent endpoint is used.
    """
    return f"""On the locked page"""


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    session["auth"] = False
    return redirect(url_for("example1.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Used to test the session set for the login_required decorator.
    """
    if request.method == "POST":
        session["auth"] = True
        return redirect(url_for("example2.account"))

    print(session)
    return f""" 
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Title</title>
</head>
<body>
<form method='post'>
<input type='submit' value='login'/>
</form>
</body>
</html>
    """


@bp.route("/account", methods=["GET"])
@login_required(session_bool_key="example1_auth", on_error_endpoint="example2.login")
def account():
    """
    This page is protected by the login_required decorator, with the login page endpoint set.
    """
    return f"""Account Page {session}"""
