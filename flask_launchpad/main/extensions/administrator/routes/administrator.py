from flask import render_template

from flask_launchpad.main.builtins.functions.security import login_required
from .. import bp
from .. import struc


@bp.route("/", methods=["GET"])
@login_required("auth", "account.login")
def administrator():
    render = "renders/index.html"
    extend = struc.extend + "base.html"

    return render_template(render, structure=struc.name, extend=extend)
