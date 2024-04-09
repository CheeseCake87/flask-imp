from flask import render_template

from .. import bp


@bp.route("/", methods=["GET"])
def index_from_object():
    return render_template(bp.tmpl("index.html"))
