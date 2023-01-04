from flask import render_template

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return render_template(bp.tmpl("index.html"))


@bp.route("/static", methods=["GET"])
def static_test():
    return render_template(bp.tmpl("static.html"))
