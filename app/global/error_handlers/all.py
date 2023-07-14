from .. import bp
from flask import render_template


@bp.errorhandler(400)
def system_400(error):
    render = f"/400.html"
    return render_template(
        render,
    ), 400


@bp.errorhandler(401)
def system_401(error):
    render = f"/401.html"
    return render_template(
        render,
    ), 401


@bp.errorhandler(403)
def system_403(error):
    render = f"/403.html"
    return render_template(
        render,
    ), 403


@bp.errorhandler(404)
def system_404(error):
    return "404", 404


@bp.errorhandler(405)
def system_405(error):
    render = f"/405.html"
    return render_template(
        render,
    ), 405


@bp.errorhandler(500)
def system_500(error):
    render = f"/500.html"
    return render_template(
        render,
    ), 500
