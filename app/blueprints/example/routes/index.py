from flask import render_template
from flask import url_for
from app import bigapp
import requests

from app.blueprints.example import bp

# \/\/ this is getting the global structure from the __init__ file
from app.blueprints.example import stru


@bp.route("/", methods=["GET"])
def index():
    resp = requests.get(f"http://127.0.0.1:5000{url_for('example2.index')}")

    print(resp)

    extend = bigapp.tmpl(stru, "extends/main.html")
    footer = bigapp.tmpl("bigapp_default", "includes/footer.html")

    return bp.scoped_render_template("renders/index.html", extend=extend, footer=footer)
