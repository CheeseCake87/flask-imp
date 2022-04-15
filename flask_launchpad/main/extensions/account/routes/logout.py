from .. import bp
from .. import config
from flask import session
from flask import redirect
from flask import url_for


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    for key, value in config["init_session"].items():
        if value == "False":
            value = False
        if value == "True":
            value = True
        session[key] = value
    return redirect(url_for("account.login"))
