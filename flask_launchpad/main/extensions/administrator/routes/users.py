from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from ....builtins.functions.auth import generate_private_key
from ....builtins.functions.auth import generate_salt
from ....builtins.functions.auth import safe_username
from ....builtins.functions.auth import sha_password
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.security import login_required
from ....builtins.functions.memberships import get_company_membership_from_user_id
from ....builtins.functions.memberships import get_user_ids_from_company_id_list
from ....builtins.functions.memberships import get_permission_membership_from_user_id

from .. import FlCompanyMembership
from .. import FlUser
from .. import bp
from .. import sql_do
from .. import struc


@bp.route("/users", methods=["GET", "POST"])
@login_required("auth", "account.login")
def users():
    if request.method == "GET":
        error = session["error"]
        message = session["message"]
        render = "renders/users.html"
        structure = struc.name()
        extend = struc.extend("backend.html")
        footer = struc.include("footer.html")

        company_list = get_company_membership_from_user_id(session["user_id"])
        company_ids = []
        company_names = []

        for value in company_list:
            company_ids.append(value[0])
            company_names.append(value[1])

        if "__system__" in company_names:
            company_users = sql_do.query(FlUser).all()
        else:
            all_users_in_company = get_user_ids_from_company_id_list(company_ids)
            company_users = sql_do.query(FlUser).filter(FlUser.user_id.in_(all_users_in_company)).all()

        user_dict = {}

        for user in company_users:
            user_dict[user.user_id] = {}
            user_dict[user.user_id]["username"] = user.username
            user_dict[user.user_id]["disabled"] = user.disabled
            user_dict[user.user_id]["permissions"] = get_permission_membership_from_user_id(user.user_id)

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
            company_names=company_names
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
