from flask import render_template

from .. import bp


@bp.route("/", methods=["GET"])
def index_test():
    return render_template(bp.tmpl("index.html"))
