from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from ...._flask_launchpad.src.flask_launchpad import model_class
from ...._flask_launchpad.src.flask_launchpad import sql_do

from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.security import login_required

from .. import bp
from .. import struc

FlPermission = model_class("FlPermission")


@bp.route("/permissions", methods=["GET", "POST"])
@login_required("auth", "account.login")
def permissions():
    error = session["error"]
    message = session["message"]
    render = "renders/permissions.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    if request.method == "POST":
        add_permission = FlPermission(
            name=request.form["name"].lower(),
            type=request.form["type"].lower()
        )
        sql_do.add(add_permission)
        sql_do.commit()
        return redirect(url_for("administrator.permissions"))

    all_permissions = sql_do.query(
        FlPermission
    ).all()

    permission_dict = {}

    for value in all_permissions:
        permission_dict[value.permission_id] = {
            "name": value.name,
            "type": value.type,
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
        all_permissions=permission_dict,
    )
