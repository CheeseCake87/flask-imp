from flask import redirect
from flask import session
from flask import url_for

from .. import bp
from ....builtins.functions.security import login_required


@bp.route("/clear-session", methods=["GET"])
@login_required("auth", "account.login")
def clear_session():
    session.clear()
    return redirect(url_for("account.login"))
