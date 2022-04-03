from functools import wraps
from flask import session
from flask import url_for
from flask import redirect
from flask import request
from flask import current_app
from werkzeug.routing import BuildError


def login_required(on_error_endpoint: str = None):
    def login_required_wrapper(func):
        @wraps(func)
        def secure_function(*args, **kwargs):
            if on_error_endpoint is None:
                return redirect(url_for("system.redirect_catch_all", message="on_error_endpoint not in args"))
            try:
                error = url_for(on_error_endpoint)
            except BuildError:
                return redirect(url_for("system.redirect_catch_all", tried=on_error_endpoint))
            return func(*args, **kwargs)
        return secure_function
    return login_required_wrapper
