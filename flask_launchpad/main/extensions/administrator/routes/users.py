from flask_launchpad.main.builtins.functions.security import login_required
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.auth import generate_salt
from ....builtins.functions.auth import generate_private_key
from ....builtins.functions.auth import sha_password
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


@bp.route("/users", methods=["GET", "POST"])
def users():
    error = session["error"]
    message = session["message"]
    render = "renders/users.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    if request.method == "POST":
        if not safe_username(request.form["username"].lower()):
            session["error"] = "Username cannot contain any special characters"
            return redirect(url_for("administrator.users"))

        check_username = sql_do.query(
            FlUser
        ).filter(
            FlUser.username == request.form["username"].lower()
        ).first()
        if check_username:
            session["error"] = "Username already exists"
            return redirect(url_for("administrator.users"))

        salt = generate_salt()
        private_key = generate_private_key(salt)
        add_user = FlUser(
            username=request.form["username"].lower(),
            password=sha_password(request.form["password"], salt),
            salt=salt,
            private_key=private_key,
            disabled=False
        )
        sql_do.add(add_user)
        sql_do.flush()
        add_membership = FlMembership(
            user_id=add_user.user_id,
            group_id=request.form["group_id"]
        )
        sql_do.add(add_membership)
        sql_do.commit()
        return redirect(url_for("administrator.users"))

    all_users = sql_do.query(
        FlUser
    ).all()

    user_dict = {}

    for v in all_users:
        permissions = sql_do.query(
            FlMembership
        ).filter(
            FlMembership.user_id == v.user_id
        ).all()

        user_dict[v.user_id] = {
            "username": v.username,
            "groups": [],
            "disabled": v.disabled
        }
        for iv in permissions:
            groups = sql_do.query(
                FlGroup
            ).filter(
                FlGroup.group_id == iv.group_id
            ).all()
            for iiv in groups:
                user_dict[v.user_id]["groups"].append((iiv.group_id, iiv.group_name))

    all_groups = sql_do.query(
        FlGroup
    ).all()

    group_dict = {}

    for value in all_groups:
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
        all_users=user_dict,
        all_groups=group_dict,
    )
