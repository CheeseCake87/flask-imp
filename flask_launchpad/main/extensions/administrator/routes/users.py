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
from ....builtins.functions.utilities import reverse_dict
from ....builtins.functions.security import login_required
from ....builtins.functions.memberships import get_company_membership_from_user_id
from ....builtins.functions.memberships import get_user_ids_from_company_id_list
from ....builtins.functions.memberships import get_permission_membership_from_user_id
from ....builtins.functions.memberships import get_permission_id_from_permission_name
from ....builtins.functions.memberships import get_all_companies

from .. import bp
from .. import sql_do
from .. import struc
from .. import FlUser
from .. import FlPermissionMembership
from .. import FlCompanyMembership


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

        if "system" in session["permissions"]:
            logged_in_company_membership = get_all_companies()
        else:
            logged_in_company_membership = get_company_membership_from_user_id(session["user_id"])

        company_ids, company_names = [], []

        for company_name, company_id in logged_in_company_membership.items():
            company_names.append(company_name)
            company_ids.append(company_id)

        company_users = get_user_ids_from_company_id_list(company_ids)

        users_in_company = sql_do.query(FlUser).filter(
            FlUser.user_id.in_(company_users)
        )

        user_dict = {}
        for user in users_in_company:
            user_dict[user.user_id] = {}
            user_dict[user.user_id]["username"] = user.username
            user_dict[user.user_id]["disabled"] = user.disabled
            user_dict[user.user_id]["permissions"] = get_permission_membership_from_user_id(user.user_id)
            user_dict[user.user_id]["companies"] = get_company_membership_from_user_id(user.user_id)

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
            all_companies=reverse_dict(logged_in_company_membership)
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

        if "company" not in request.form:
            company_membership = get_company_membership_from_user_id(session["user_id"])
            for company_name, company_id in company_membership.items():
                add_company_membership = FlCompanyMembership(
                    company_id=company_id,
                    user_id=add_user.user_id
                )
                sql_do.add(add_company_membership)
        else:
            add_company_membership = FlCompanyMembership(
                company_id=request.form["company"],
                user_id=add_user.user_id
            )
            sql_do.add(add_company_membership)
            print(request.form["company"])

        sql_do.commit()
        return redirect(url_for("administrator.users"))
