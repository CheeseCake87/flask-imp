from flask_launchpad.main.builtins.functions.security import login_required
from .. import bp
from .. import struc
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for


@bp.route("/", methods=["GET"])
def administrator():
    render = "renders/index.html"
    extend = struc.extend + "base.html"

    return render_template(render, structure=struc.name, extend=extend)
