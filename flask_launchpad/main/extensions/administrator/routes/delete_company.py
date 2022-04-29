from flask import redirect
from flask import url_for

from ....builtins.functions.security import login_required

from .. import FlCompany
from .. import FlCompanyMembership
from .. import bp
from .. import sql_do


@bp.route("/company/delete/<company_id>", methods=["GET"])
@login_required("auth", "account.login")
def delete_company(company_id):
    sql_do.query(FlCompanyMembership).filter(
        FlCompanyMembership.company_id == company_id
    ).delete()

    sql_do.query(FlCompany).filter(
        FlCompany.company_id == company_id
    ).delete()

    sql_do.commit()
    return redirect(url_for("administrator.companies"))
