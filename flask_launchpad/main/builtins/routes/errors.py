from flask import current_app
from flask import Response
from flask import session
from flask import request
from flask import render_template


@current_app.errorhandler(404)
def request_404(error):
    render_args = {
        "template_name_or_list": "renders/error.html",
        "structure": "structures/default.html",
        "title": "404 Error! Page not found",
        "keywords": "Error, Page, Not, Found",
        "description": "Error, page not found"
    }
    debug_args = {
        "debug": session,
        "error": error,
        "this_path": request.path
    }
    return render_template(**render_args, **debug_args), 404


@current_app.errorhandler(401)
def custom_401(error):
    return Response('You are unauthorized to access this resource.', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})
