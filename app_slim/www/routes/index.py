from flask import render_template, session

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    print(session)
    return render_template(bp.tmpl("index.html"))
