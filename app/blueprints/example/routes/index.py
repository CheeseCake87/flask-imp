from flask import render_template
from app import bigapp

from app.blueprints.example import bp

# \/\/ this is getting the global structure from the __init__ file
from app.blueprints.example import stru


@bp.route("/", methods=["GET"])
def index():
    """
    Shows an example of the structure (theme) working
    """

    render = bp.render("index.html")
    extend = bigapp.extend(stru, "main.html")
    footer = bigapp.include("bigapp_default", "footer.html")

    return render_template(render, extend=extend, footer=footer)
