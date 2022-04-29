from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from ....builtins.functions.security import login_required

from .. import FlCompany
from .. import bp
from .. import sql_do
from .. import struc


@bp.route("/companies", methods=["GET", "POST"])
@login_required("auth", "account.login")
def companies():
    error = session["error"]
    message = session["message"]
    render = "renders/companies.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    if request.method == "POST":
        add_company = FlCompany(
            name=request.form["name"].lower(),
        )
        sql_do.add(add_company)
        sql_do.commit()
        return redirect(url_for("administrator.companies"))

    all_companies = sql_do.query(
        FlCompany
    ).all()

    company_dict = {}

    for value in all_companies:
        company_dict[value.company_id] = {
            "name": value.name
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
        all_companies=company_dict,
    )
