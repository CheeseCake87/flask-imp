from flask import url_for
from flask import redirect

from ....builtins.functions.security import login_required

from .. import bp


@bp.route("/", methods=["GET"])
@login_required("auth", "account.login")
def system():
    return redirect(url_for("account.dashboard"))
