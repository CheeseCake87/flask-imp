from flask import Response
from flask import current_app


@current_app.before_request
def before_request():
    pass


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
