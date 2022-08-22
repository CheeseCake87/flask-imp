from flask import render_template

from .. import bp, page_needs


@bp.route("/structure-example", methods=["GET"])
def home_page():
    render = bp.tmpl("structure-example.html")
    return render_template(render, **page_needs)
