from flask import current_app
from flask import render_template

STRUCTURE = "default_theme"


@current_app.errorhandler(400)
def system_400(error):
    render = f"{STRUCTURE}/errors/error-400.html"
    return render_template(
        render, extend=f"{STRUCTURE}/extends/error.html"
    ), 400


@current_app.errorhandler(401)
def system_401(error):
    render = f"{STRUCTURE}/errors/error-401.html"
    return render_template(
        render, extend=f"{STRUCTURE}/extends/error.html"
    ), 401


@current_app.errorhandler(403)
def system_403(error):
    render = f"{STRUCTURE}/errors/error-403.html"
    return render_template(
        render, extend=f"{STRUCTURE}/extends/error.html"
    ), 403


@current_app.errorhandler(404)
def system_404(error):
    render = f"{STRUCTURE}/errors/error-404.html"
    return render_template(
        render, extend=f"{STRUCTURE}/extends/error.html"
    ), 404


@current_app.errorhandler(405)
def system_405(error):
    render = f"{STRUCTURE}/errors/error-405.html"
    return render_template(
        render, extend=f"{STRUCTURE}/extends/error.html"
    ), 405


@current_app.errorhandler(500)
def system_500(error):
    render = f"{STRUCTURE}/errors/error-500.html"
    return render_template(
        render, extend=f"{STRUCTURE}/extends/error.html"
    ), 500
