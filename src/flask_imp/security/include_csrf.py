from functools import wraps

from flask import abort
from flask import request
from flask import session

from flask_imp.auth import generate_csrf_token


def include_csrf(
    session_key: str = "csrf", form_key: str = "csrf", abort_code: int = 401
):
    """
    A decorator that handles CSRF protection.

    :raw-html:`<br />`

    On a **GET** request, a CSRF token is generated and stored in the session key
    specified by the session_key parameter.

    On a **POST** request, the form_key specified is checked against the session_key
    specified.

    :raw-html:`<br />`

    | If they match, the request is allowed to continue.
    | If no match, the response will be abort(abort_code), default 401.

    :raw-html:`<br />`

    .. code-block::

        @bp.route("/admin", methods=["GET", "POST"])
        @include_csrf(session_key="csrf", form_key="csrf")
        def admin_page():
            ...
            # You must pass in the CSRF token from the session into the template.
            # Then add <input type="hidden" name="csrf" value="{{ csrf }}"> to the form.
            return render_template("admin.html", csrf=session.get("csrf"))

    :raw-html:`<br />`

    -----

    :param session_key: The session key to store the CSRF token in.
    :param form_key: The form key to check against the session key.
    :param abort_code: The abort code to use if the CSRF check fails.
    :return: The decorated function, or abort(abort_code).
    """

    def include_csrf_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if request.method == "GET":
                session[session_key] = generate_csrf_token()

                return func(*args, **kwargs)

            if request.method == "POST":
                _session_key = session.get(session_key)
                _form_key = request.form.get(form_key)

                if _form_key is None:
                    return abort(abort_code)

                if _session_key is None:
                    return abort(abort_code)

                if _session_key != _form_key:
                    return abort(abort_code)

            return func(*args, **kwargs)

        return inner

    return include_csrf_wrapper
