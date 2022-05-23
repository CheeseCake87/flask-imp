from flask import redirect
from flask import url_for
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

from ....builtins.functions.security import login_required

from .. import bp


@bp.route("/database/drop_all", methods=["GET"])
@login_required("auth", "account.login")
def database_drop_all():
    for module_name, module in current_app.config["SHARED_MODELS"].items():
        SQLAlchemy.drop_all(module)
    return redirect(url_for("system.database"))


@bp.route("/database/drop/<module>", methods=["GET"])
@login_required("auth", "account.login")
def database_drop(module):
    try:
        SQLAlchemy.drop_all(current_app.config["SHARED_MODELS"][module])
    except KeyError:
        return redirect(url_for("system.database"))
    return redirect(url_for("system.database"))
