from flask import render_template

from .. import bp


@bp.route("/auth", methods=["GET"])
def auth_test():
    return render_template(bp.tmpl("static.html"))
