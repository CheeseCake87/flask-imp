from flask import redirect
from flask import url_for

from ....builtins.functions.security import login_required

from .. import FlCompanyMembership
from .. import bp
from .. import sql_do


@bp.route("/users/edit/<user_id>/delete/company/<company_id>", methods=["GET"])
@login_required("auth", "account.login")
def delete_company_from_user(user_id, company_id):
    sql_do.query(FlCompanyMembership).filter(
        FlCompanyMembership.company_id == company_id,
        FlCompanyMembership.user_id == user_id
    ).delete()
    sql_do.commit()
    return redirect(url_for("administrator.edit_user", user_id=user_id))
