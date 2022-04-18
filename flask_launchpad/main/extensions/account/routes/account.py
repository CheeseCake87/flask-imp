from ....builtins.functions.security import login_required
from .. import bp
from flask import url_for
from flask import redirect


@bp.route("/", methods=["GET"])
@login_required("auth", "account.login")
def account():
    return redirect(url_for("account.dashboard"))
