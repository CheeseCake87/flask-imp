from flask import render_template

from .. import bp
from .. import struc
from ....builtins.functions.security import login_required


@bp.route("/", methods=["GET"])
@login_required("auth", "account.login")
def administrator():
    render = "renders/index.html"
    extend = struc.extend + "base.html"

    return render_template(render, structure=struc.name, extend=extend)
