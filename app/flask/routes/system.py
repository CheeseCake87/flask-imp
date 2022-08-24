from flask import current_app
from flask import Response
from flask import request
from flask import session


@current_app.before_request
def before_request():
    if "version" not in session:
        session["version"] = current_app.config["VERSION"]


@current_app.after_request
def after_request(response):
    return response


@current_app.errorhandler(404)
def request_404(error):
    return Response(error, 404)


@current_app.errorhandler(401)
def custom_401(error):
    return Response('You are unauthorized to access this resource.', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


@current_app.route("/errors/redirect-catch-all", endpoint="errors.redirect_catch_all")
def redirect_catch_all():
    endpoint_tried = "The endpoint does not exist"
    if "tried" in request.args:
        endpoint_tried += f"{request.args['tried']}"
    return Response(endpoint_tried)
