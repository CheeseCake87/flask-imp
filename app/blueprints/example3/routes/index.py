from flask import render_template_string, render_template
from app import bigapp

from .. import bp

# \/\/ this is getting the global structure from the __init__ file
from .. import stru


@bp.route("/", methods=["GET"])
def index():
    """
    Shows an example of the structure (theme) working
    """

    render = bp.scoped_render("renders/index.html")
    extend = bigapp.tmpl(stru, "extends/main.html")
    footer = bigapp.tmpl("bigapp_default", "includes/footer.html")

    return render_template(render, extend=extend, footer=footer)
