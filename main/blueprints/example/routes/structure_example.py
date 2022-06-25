from flask import current_app
from flask import render_template
from main import structures

from .. import bp
from .. import stru


@bp.route("/structure-example", methods=["GET"])
def home_page():
    """
    Shows an example of the structure working
    """

    render = "renders/structure_example.html"
    extend = structures.extend("main.html", stru)
    footer = structures.include("footer.html", stru)

    return render_template(render, extend=extend, footer=footer)
