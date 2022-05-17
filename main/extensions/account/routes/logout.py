from flask import session
from flask import redirect
from flask import url_for

from .. import bp
from .. import fl_bp


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    for key, value in fl_bp.config["session"].items():
        if value == "False":
            value = False
        if value == "True":
            value = True
        session[key] = value
    return redirect(url_for("account.login"))
