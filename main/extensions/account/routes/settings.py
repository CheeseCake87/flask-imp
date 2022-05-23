from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from ...._flask_launchpad.src.flask_launchpad import model_class
from ...._flask_launchpad.src.flask_launchpad import sql_do

from ....builtins.functions.auth import generate_salt
from ....builtins.functions.auth import safe_username
from ....builtins.functions.auth import sha_password
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.security import login_required

from .. import bp
from .. import struc

FlUser = model_class("FlUser")


@bp.route("/settings", methods=["GET", "POST"])
@login_required("auth", "account.login")
def settings():
    error = session["error"]
    message = session["message"]
    render = "renders/account_settings.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    query_user = sql_do.query(FlUser).filter(FlUser.user_id == session["user_id"]).first()

    if request.method == "POST":
        if "update_user" in request.form:
            if not safe_username(request.form["username"].lower()):
                session["error"] = "Username cannot contain any special characters"
                return redirect(url_for("administrator.edit_user", user_id=query_user.user_id))

            if request.form["username"] != query_user.username:
                check_username = sql_do.query(FlUser).filter(
                    FlUser.username == request.form["username"].lower()
                ).first()
                if check_username:
                    session["error"] = "Username already exists"
                    return redirect(url_for("administrator.edit_user", user_id=query_user.user_id))

                query_user.username = request.form["username"].lower()

            if request.form["new_password"] != "":
                salt = generate_salt()
                query_user.salt = salt
                query_user.password = sha_password(request.form["new_password"], salt)

            sql_do.commit()
            session["message"] = "User has been updated"
            return redirect(url_for("administrator.edit_user", user_id=query_user.user_id))

    user_dict = {
        "user_id": query_user.user_id,
        "username": query_user.username,
        "disabled": query_user.disabled
    }

    return render_template(
        render,
        structure=structure,
        extend=extend,
        footer=footer,
        error=error,
        clear_error=clear_error(),
        message=message,
        clear_message=clear_message(),
        user=user_dict,
        endpoints={},
    )
