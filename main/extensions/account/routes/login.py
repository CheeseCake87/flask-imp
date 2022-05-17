from flask import render_template
from flask import session
from flask import redirect
from flask import request
from flask import url_for
from flask import current_app

from ....builtins.functions.security import logged_in_check
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.auth import safe_username
from ....builtins.functions.auth import auth_password

from .. import bp
from .. import struc
from .. import sql_do
from .. import FlUser


@bp.route("/login", methods=["GET", "POST"])
@logged_in_check("auth", "account.dashboard")
def login():
    from ....builtins.functions.memberships import get_permission_membership_from_user_id

    error = session["error"]
    message = session["message"]
    render = "renders/login.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    if request.method == "POST":
        if not safe_username(request.form["username"]):
            session["error"] = "Username or password incorrect"
            return redirect(url_for("account.login"))

        query_user = sql_do.query(FlUser).filter(FlUser.username == request.form["username"]).first()
        if query_user is None:
            session["error"] = "Username or password incorrect"
            return redirect(url_for("account.login"))

        if auth_password(input_password=request.form["password"],
                         database_password=query_user.password,
                         database_salt=query_user.salt):
            session["auth"] = True
            session["user_id"] = query_user.user_id
            session["username"] = query_user.username
            session["permissions"] = get_permission_membership_from_user_id(query_user.user_id)
            return redirect(url_for(current_app.config["LOGIN_DASHBOARD"]))

        return redirect(url_for("account.login"))

    return render_template(
        render,
        structure=structure,
        extend=extend,
        footer=footer,
        error=error,
        clear_error=clear_error(),
        message=message,
        clear_message=clear_message(),
        form_elements=["input"]
    )
