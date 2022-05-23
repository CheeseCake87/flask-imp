from flask import render_template
from flask import current_app

from ....builtins.functions.database import get_tables
from ....builtins.functions.security import login_required

from .. import bp
from .. import struc


@bp.route("/database", methods=["GET"])
@login_required("auth", "account.login")
def database():
    render = "renders/database.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    models = get_tables()

    return render_template(
        render,
        structure=structure,
        extend=extend,
        footer=footer,
        models=models,
        shared_models=current_app.config["SHARED_MODELS"]
    )
