from flask import render_template

from .. import bp, page_needs


@bp.route("/example2", methods=["GET"])
def index():
    render = bp.tmpl("index.html")
    return render_template(render, **page_needs)
