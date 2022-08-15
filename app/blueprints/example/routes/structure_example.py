from flask import render_template
from app import bigapp

from app.blueprints.example import bp
from app.blueprints.example import stru


@bp.route("/structure-example", methods=["GET"])
def home_page():
    """
    Shows an example of the structure working
    """

    render = bp.render("structure-example.html")
    extend = bigapp.extend("main.html", stru)
    footer = bigapp.include("footer.html", stru)

    return render_template(render, extend=extend, footer=footer)
