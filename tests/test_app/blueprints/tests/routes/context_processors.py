from flask import render_template

from .. import bp


@bp.route("/context-processors", methods=["GET"])
def context_processors_test():
    return render_template(bp.tmpl("context_processors.html"))
