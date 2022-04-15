from ....builtins.functions.security import login_required
from ....builtins.functions.database import get_tables
from ....builtins.functions.database import has_table
from .. import bp
from .. import struc
import sys
import inspect
from flask import request
from flask import current_app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


@bp.route("/database", methods=["GET"])
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
        models=models
    )
