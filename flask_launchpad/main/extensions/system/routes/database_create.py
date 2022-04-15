from ....builtins.functions.security import login_required
from .. import bp
from flask import redirect
from flask import url_for
from flask import current_app
from flask_sqlalchemy import SQLAlchemy


@bp.route("/database/create_all/<forward>", methods=["GET"])
def database_create_all(forward):
    for module_name, module in current_app.config["SHARED_MODELS"].items():
        SQLAlchemy.create_all(module)
    return redirect(url_for(forward))


@bp.route("/database/create/<module>", methods=["GET"])
def database_create(module):
    try:
        SQLAlchemy.create_all(current_app.config["SHARED_MODELS"][module])
    except KeyError:
        return redirect(url_for("system.database"))
    return redirect(url_for("system.database"))
