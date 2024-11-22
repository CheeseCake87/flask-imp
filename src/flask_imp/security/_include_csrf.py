import typing as t
from functools import wraps

from flask import abort
from flask import request
from flask import session
from flask_imp.auth import generate_csrf_token


def include_csrf(
    session_key: str = "csrf", form_key: str = "csrf", abort_status: int = 401
) -> t.Callable[..., t.Any]:
    """
    A decorator that handles CSRF protection.

    On a **GET** request, a CSRF token is generated and stored in the session key
    specified by the session_key parameter.

    On a **POST** request, the form_key specified is checked against the session_key
    specified.

    If they match, the request is allowed to continue.

    If no match, the response will be aborted, flask.abort(abort_code), default 401.

    Example of a route that requires CSRF protection::

        @bp.route("/admin", methods=["GET", "POST"])
        @include_csrf(session_key="csrf", form_key="csrf")
        def admin_page():
            ...
            # You must pass in the CSRF token from the session into the template.
            # Then add <input type="hidden" name="csrf" value="{{ csrf }}"> to the form.
            return render_template("admin.html", csrf=session.get("csrf"))

    :param session_key: session key to store the CSRF token in.
    :param form_key: form key to check against the session key.
    :param abort_status: abort status code to use if the CSRF check fails.
    :return: decorated function, or abort(abort_code) response.
    """

    def include_csrf_wrapper(func: t.Any) -> t.Callable[..., t.Any]:
        @wraps(func)
        def inner(*args: t.Any, **kwargs: t.Any) -> t.Any:
            if request.method == "GET":
                session[session_key] = generate_csrf_token()

                return func(*args, **kwargs)

            if request.method == "POST":
                _session_key = session.get(session_key)
                _form_key = request.form.get(form_key)

                if _form_key is None:
                    return abort(abort_status)

                if _session_key is None:
                    return abort(abort_status)

                if _session_key != _form_key:
                    return abort(abort_status)

            return func(*args, **kwargs)

        return inner

    return include_csrf_wrapper
