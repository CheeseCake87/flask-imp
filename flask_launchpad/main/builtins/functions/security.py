from functools import wraps
from flask import session
from flask import url_for
from flask import redirect
from werkzeug.routing import BuildError


def login_required(session_bool_key: str, on_error_endpoint: str):
    def login_required_wrapper(func):
        @wraps(func)
        def secure_function(*args, **kwargs):

            if on_error_endpoint == "":
                return redirect(url_for("system.redirect_catch_all", message="on_error_endpoint not in args"))

            try:
                url_for(on_error_endpoint)
            except BuildError:
                return redirect(url_for("system.redirect_catch_all", tried=on_error_endpoint))

            if session_bool_key not in session:
                return redirect(url_for(on_error_endpoint))

            if not session[session_bool_key]:
                return redirect(url_for(on_error_endpoint))

            return func(*args, **kwargs)
        return secure_function
    return login_required_wrapper
