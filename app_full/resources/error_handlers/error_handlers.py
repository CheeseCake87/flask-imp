from flask import current_app as app

from flask import render_template


@app.errorhandler(400)
def bad_request(e):
    return render_template(
        "error.html",
        error_code=400,
        error_message="The request is invalid.",
    ), 400


@app.errorhandler(401)
def unauthorized(e):
    return render_template(
        "error.html",
        error_code=401,
        error_message="You are not authorized to access this page.",
    ), 401


@app.errorhandler(403)
def forbidden(e):
    return render_template(
        "error.html",
        error_code=403,
        error_message="You do not have permission to access this page.",
    ), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "error.html",
        error_code=404,
        error_message="The page you are looking for does not exist.",

    ), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template(
        "error.html",
        error_code=405,
        error_message="The method is not allowed for the requested URL.",
    ), 405


@app.errorhandler(410)
def gone(e):
    return render_template(
        "error.html",
        error_code=410,
        error_message="This page is no longer available.",
    ), 410


@app.errorhandler(429)
def too_many_requests(e):
    return render_template(
        "error.html",
        error_code=429,
        error_message="You have made too many requests.",
    ), 429


@app.errorhandler(500)
def server_error(e):
    return render_template(
        "error.html",
        error_code=500,
        error_message="An internal server error has occurred.",
    ), 500
