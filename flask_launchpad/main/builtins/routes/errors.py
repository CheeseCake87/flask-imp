from flask import current_app
from flask import Response
from flask import session
from flask import request
from flask import render_template
from markupsafe import Markup


@current_app.errorhandler(404)
def request_404(error):
    render = "renders/error.html"
    extend = "structures/system/notice.html"
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


@current_app.route("/errors/redirect-catch-all", endpoint="errors.redirect_catch_all")
def redirect_catch_all():
    re_var = """
    This is a redirect catch all.
    """
    if "tried" in request.args:
        re_var = f"""
        The endpoint: {request.args['tried']} does not exist
        """
    return Markup(re_var)
