from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from ....builtins.functions.auth import generate_salt
from ....builtins.functions.auth import safe_username
from ....builtins.functions.auth import sha_password
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.utilities import reverse_dict
from ....builtins.functions.security import login_required
from ....builtins.functions.memberships import get_permission_membership_from_user_id

from .. import FlPermission
from .. import FlPermissionMembership
from .. import FlUser
from .. import bp
from .. import sql_do
from .. import struc


@bp.route("/users/edit/<user_id>", methods=["GET", "POST"])
@login_required("auth", "account.login")
def edit_user(user_id):
    query_user = sql_do.query(FlUser).filter(
        FlUser.user_id == user_id
    ).first()

    if "system" in session["permissions"]:
        logged_in_company_membership = get_all_companies()
    else:
        logged_in_company_membership = get_company_membership_from_user_id(session["user_id"])

    query_user_company_membership = get_company_membership_from_user_id(query_user.user_id)
    for company_name in query_user_company_membership:
        if company_name not in logged_in_company_membership:
            redirect("account.users")

    if request.method == "GET":
        error = session["error"]
        message = session["message"]
        render = "renders/edit_user.html"
        structure = struc.name()
        extend = struc.extend("backend.html")
        footer = struc.include("footer.html")

        query_user_permissions = get_permission_membership_from_user_id(query_user.user_id)

        user_dict = {
            "user_id": query_user.user_id,
            "username": query_user.username,
            "permissions": query_user_permissions,
            "companies": query_user_company_membership,
            "disabled": query_user.disabled
        }

        all_permissions = sql_do.query(FlPermission).all()
        permission_dict = {}
        for value in all_permissions:
            if value.name not in query_user_permissions:
                permission_dict[value.permission_id] = value.name

        all_companies = sql_do.query(FlCompany).all()
        company_dict = {}
        for value in all_companies:
            if value.name not in query_user_company_membership:
                company_dict[value.company_id] = value.name

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
            all_permissions=permission_dict,
            available_companies=company_dict
        )

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

        if "add_permission" in request.form:
            add_permission = FlPermissionMembership(
                user_id=query_user.user_id,
                permission_id=request.form["permission_id"]
            )
            sql_do.add(add_permission)
            sql_do.commit()
            return redirect(url_for("administrator.edit_user", user_id=user_id))

        if "add_company" in request.form:
            add_company = FlCompanyMembership(
                user_id=query_user.user_id,
                company_id=request.form["company_id"]
            )
            sql_do.add(add_company)
            sql_do.commit()
            return redirect(url_for("administrator.edit_user", user_id=user_id))

        return redirect(url_for("administrator.edit_user", user_id=user_id))
