from flask import render_template
from flask import session

from ....builtins.functions.security import login_required

from .. import bp
from .. import struc


@bp.route("/session", methods=["GET"])
@login_required("auth", "account.login")
def session():
    render = "renders/session.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    return render_template(
        render,
        structure=structure,
        extend=extend,
        footer=footer,
        session=session
    )
