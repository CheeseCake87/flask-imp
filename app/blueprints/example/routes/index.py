from flask import render_template, session

from .. import bp, page_needs


@bp.route("/", methods=["GET"])
def index():
    render = bp.tmpl("index.html")
    print(session)
    return render_template(render, **page_needs)
