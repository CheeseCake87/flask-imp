from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from ...._flask_launchpad.src.flask_launchpad import model_class
from ...._flask_launchpad.src.flask_launchpad import sql_do

from ....builtins.functions.auth import generate_private_key
from ....builtins.functions.auth import generate_salt
from ....builtins.functions.auth import safe_username
from ....builtins.functions.auth import sha_password
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.security import login_required
from ....builtins.functions.database import convert_sql_to_list_dict

from .. import bp
from .. import struc

FlUser = model_class("FlUser")
FlPermissionMembership = model_class("FlPermissionMembership")


@bp.route("/users", methods=["GET", "POST"])
@login_required("auth", "account.login")
def users():
    from ....builtins.functions.memberships import get_permission_id_from_permission_name

    if request.method == "GET":
        error = session["error"]
        message = session["message"]
        render = "renders/users.html"
        structure = struc.name()
        extend = struc.extend("backend.html")
        footer = struc.include("footer.html")

        user_dict = convert_sql_to_list_dict(sql_do.query(FlUser).all())

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
        )

    if request.method == "POST":
        if not safe_username(request.form["username"].lower()):
            session["error"] = "Username cannot contain any special characters"
            return redirect(url_for("administrator.users"))

        check_username = sql_do.query(FlUser).filter(
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

        default_permission_id = get_permission_id_from_permission_name("user")
        add_permission_membership = FlPermissionMembership(
            user_id=add_user.user_id,
            permission_id=default_permission_id
        )
        sql_do.add(add_permission_membership)

        sql_do.commit()
        return redirect(url_for("administrator.users"))
