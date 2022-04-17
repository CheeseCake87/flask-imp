from ....builtins.functions.security import login_required
from ....builtins.functions.utilities import clear_error
from ....builtins.functions.utilities import clear_message
from .. import bp
from .. import struc
from flask import request
from flask import current_app
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy


@bp.route("/", methods=["GET", "POST"])
def uploads():
    error = session["error"]
    message = session["message"]
    render = "renders/setup.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")

    return render_template(
        render,
        structure=structure,
        extend=extend,
        footer=footer,
        error=error,
        clear_error=clear_error(),
        message=message,
        clear_message=clear_message()
    )
