from flask import render_template_string, render_template
from app import structures

from .. import bp, page_needs


@bp.route("/", methods=["GET"])
def index():
    render = bp.tmpl("index.html")
    return render_template(render, **page_needs)
