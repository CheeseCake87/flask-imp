from flask import current_app
from flask import Response
from flask import session
from flask import request
from flask import render_template


@current_app.errorhandler(404)
def request_404(error):
    render = "renders/error.html"
    extend = "structures/system/page_message.html"
    set_theme = "system"

    debug_args = {
        "debug": session,
        "error": error,
        "this_path": request.path
    }
    return render_template(render, extend=extend, set_theme=set_theme, **debug_args), 404


@current_app.errorhandler(401)
def custom_401(error):
    return Response('You are unauthorized to access this resource.', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})
