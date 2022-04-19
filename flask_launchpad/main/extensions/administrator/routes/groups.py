from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from .. import FlGroup
from .. import bp
from .. import sql_do
from .. import struc
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.security import login_required


@bp.route("/groups", methods=["GET", "POST"])
@login_required("auth", "account.login")
def groups():
    error = session["error"]
    message = session["message"]
    render = "renders/groups.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    if request.method == "POST":
        add_group = FlGroup(
            group_name=request.form["group_name"].lower(),
            group_type=request.form["group_type"].lower()
        )
        sql_do.add(add_group)
        sql_do.commit()
        return redirect(url_for("administrator.groups"))

    all_groups = sql_do.query(
        FlGroup
    ).all()

    group_dict = {}

    for value in all_groups:
        group_dict[value.group_id] = {
            "group_name": value.group_name,
            "group_type": value.group_type,
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
        all_groups=group_dict,
    )
