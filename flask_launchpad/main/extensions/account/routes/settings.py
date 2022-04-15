from flask_launchpad.main.builtins.functions.security import login_required
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.auth import sha_password
from ....builtins.functions.auth import generate_salt
from ....builtins.functions.auth import generate_private_key
from ....builtins.functions.auth import safe_username
from .. import bp
from .. import struc
from .. import sql_do
from .. import FlUser
from .. import FlGroup
from .. import FlMembership
from flask import render_template
from sqlalchemy import desc
from flask import request
from flask import session
from flask import redirect
from flask import url_for


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    error = session["error"]
    message = session["message"]
    render = "renders/settings.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    query_user = sql_do.query(
        FlUser
    ).filter(
        FlUser.user_id == session["user_id"]
    ).first()

    if request.method == "POST":
        if "update_user" in request.form:
            if not safe_username(request.form["username"].lower()):
                session["error"] = "Username cannot contain any special characters"
                return redirect(url_for("administrator.edit_user", user_id=user_id))

            if request.form["username"] != query_user.username:
                check_username = sql_do.query(
                    FlUser
                ).filter(
                    FlUser.username == request.form["username"].lower()
                ).first()
                if check_username:
                    session["error"] = "Username already exists"
                    return redirect(url_for("administrator.edit_user", user_id=user_id))

                query_user.username = request.form["username"].lower()

            if request.form["new_password"] != "":
                salt = generate_salt()
                query_user.salt = salt
                query_user.password = sha_password(request.form["new_password"], salt)

            sql_do.commit()
            session["message"] = "User has been updated"
            return redirect(url_for("administrator.edit_user", user_id=user_id))

        if "add_group" in request.form:
            add_membership = FlMembership(
                user_id=query_user.user_id,
                group_id=request.form["group_id"]
            )
            sql_do.add(add_membership)
            sql_do.commit()
            return redirect(url_for("administrator.edit_user", user_id=user_id))


    group_dict = {}

    membership = sql_do.query(
        FlMembership
    ).filter(
        FlMembership.user_id == query_user.user_id
    ).all()

    user_dict = {
        "user_id": query_user.user_id,
        "username": query_user.username,
        "groups": [],
        "disabled": query_user.disabled
    }
    group_list = []
    for iv in membership:
        groups = sql_do.query(
            FlGroup
        ).filter(
            FlGroup.group_id == iv.group_id
        ).all()
        for iiv in groups:
            group_list.append(iiv.group_name)
            user_dict["groups"].append((iiv.group_id, iiv.group_name))

    all_groups = sql_do.query(
        FlGroup
    ).all()

    for value in all_groups:
        if value.group_name not in group_list:
            group_dict[value.group_id] = value.group_name

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
        all_groups=group_dict,
    )
