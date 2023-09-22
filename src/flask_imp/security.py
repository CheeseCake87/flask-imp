import typing as t
from functools import wraps
from functools import partial

from flask import flash
from flask import abort
from flask import redirect
from flask import session
from flask import url_for
from flask import request

from flask_imp import Auth


def _check_against_values_allowed(
        session_value: t.Union[list, str, int, bool],
        values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
) -> bool:
    """
    Checks if the session value matches the values allowed. Used by login_check and permission_check.
    """
    if isinstance(values_allowed, list):
        if isinstance(session_value, list):
            for value in session_value:
                if value in values_allowed:
                    return True
            return False

        if session_value in values_allowed:
            return True
        return False

    if session_value == values_allowed:
        return True

    return False


def login_check(
        session_key: str,
        values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
        fail_endpoint: t.Optional[str] = None,
        pass_endpoint: t.Optional[str] = None,
        endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
        message: t.Optional[str] = None,
        message_category: str = "message"
):
    """
    A decorator that checks if the specified session key exists and contains the specified value.

    :raw-html:`<br />`

    **Example of a route that requires a user to be logged in:**

    :raw-html:`<br />`

    .. code-block::

        @bp.route("/admin", methods=["GET"])
        @login_check('logged_in', True, fail_endpoint='blueprint.login_page', message="Login needed")
        def admin_page():
            ...

    :raw-html:`<br />`

    **Example of a route that if the user is already logged in, redirects to the specified endpoint:**

    :raw-html:`<br />`

    .. code-block::

        @bp.route("/login-page", methods=["GET"])
        @login_check('logged_in', True, pass_endpoint='blueprint.admin_page', message="Already logged in")
        def login_page():
            ...

    :raw-html:`<br />`

    -----

    :param session_key: The session key to check for.
    :param values_allowed: A list of or singular value(s) that the session key must contain.
    :param fail_endpoint: The endpoint to redirect to if the session key does not exist or
                          match the pass_value.
    :param pass_endpoint: The endpoint to redirect to if the session key passes.
                          Used to redirect away from login pages, if already logged in.
    :param endpoint_kwargs: A dictionary of keyword arguments to pass to the redirect endpoint.
    :param message: If a message is specified, a flash message is shown.
    :param message_category: The category of the flash message.
    :return: The decorated function, or abort(403).
    """

    def login_check_wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            skey = session.get(session_key)

            def setup_flash(_message, _message_category):
                if _message:
                    partial_flash = partial(flash, _message)
                    if _message_category:
                        partial_flash(_message_category)
                    else:
                        partial_flash()

            if skey is None:
                if fail_endpoint:
                    setup_flash(message, message_category)

                    if endpoint_kwargs:
                        return redirect(url_for(fail_endpoint, **endpoint_kwargs))

                    return redirect(url_for(fail_endpoint))

                return func(*args, **kwargs)

            if skey is not None:
                if _check_against_values_allowed(skey, values_allowed):
                    if pass_endpoint:
                        setup_flash(message, message_category)

                        if endpoint_kwargs:
                            return redirect(url_for(pass_endpoint, **endpoint_kwargs))

                        return redirect(url_for(pass_endpoint))

                    return func(*args, **kwargs)

                if fail_endpoint:
                    setup_flash(message, message_category)

                    if endpoint_kwargs:
                        return redirect(url_for(fail_endpoint, **endpoint_kwargs))

                    return redirect(url_for(fail_endpoint))

                return func(*args, **kwargs)

            return abort(403)

        return inner

    return login_check_wrapper


def permission_check(
        session_key: str,
        values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
        fail_endpoint: t.Optional[str] = None,
        endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
        message: t.Optional[str] = None,
        message_category: str = "message"
):
    """
    A decorator that checks if the specified session key exists and its value(s) match the specified value(s).

    :raw-html:`<br />`

    **Example:**

    :raw-html:`<br />`

    .. code-block::

        @bp.route("/admin-page", methods=["GET"])
        @login_check('logged_in', True, 'blueprint.login_page')  # can be mixed with login_check
        @permission_check('permissions', ['admin'], fail_endpoint='www.index', message="Failed message")
        def admin_page():
            ...

    :raw-html:`<br />`

    -----

    :param session_key: The session key to check for.
    :param values_allowed: A list of or singular value(s) that the session key must contain.
    :param fail_endpoint: The endpoint to redirect to if the
                          session key does not exist or does not contain the
                          specified values.
    :param endpoint_kwargs: A dictionary of keyword arguments to pass to the redirect endpoint.
    :param message: If a message is specified, a flash message is shown.
    :param message_category: The category of the flash message.
    :return: The decorated function, or abort(403).
    """

    def permission_check_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            skey = session.get(session_key)

            def setup_flash(_message, _message_category):
                if _message:
                    partial_flash = partial(flash, _message)
                    if _message_category:
                        partial_flash(_message_category)
                    else:
                        partial_flash()

            if skey:
                if _check_against_values_allowed(skey, values_allowed):
                    return func(*args, **kwargs)

            setup_flash(message, message_category)

            if fail_endpoint:

                if endpoint_kwargs:
                    return redirect(url_for(fail_endpoint, **endpoint_kwargs))

                return redirect(url_for(fail_endpoint))

            return abort(403)

        return inner

    return permission_check_wrapper


def api_login_check(
        session_key: str,
        values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
        fail_json: t.Optional[t.Dict[str, t.Any]] = None
):
    """
    A decorator that is used to secure API routes that return JSON responses.

    :raw-html:`<br />`

    **Example of a route that requires a user to be logged in:**

    :raw-html:`<br />`

    .. code-block::

        @bp.route("/api/resource", methods=["GET"])
        @api_login_check('logged_in', True)
        def api_page():
            ...

    :raw-html:`<br />`

    **You can also supply your own failed return JSON:**

    :raw-html:`<br />`

    .. code-block::

        @bp.route("/api/resource", methods=["GET"])
        @api_login_check('logged_in', True, fail_json={"error": "You are not logged in."})
        def api_page():
            ...

    :raw-html:`<br />`

    -----

    :param session_key: The session key to check for.
    :param values_allowed: A list of or singular value(s) that the session key must contain.
    :param fail_json: JSON that is returned on failure. {"error": "You are not logged in."} by default.
    :return: The decorated function, or a JSON response.
    """

    def api_login_check_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            skey = session.get(session_key)
            if skey:
                if _check_against_values_allowed(skey, values_allowed):
                    return func(*args, **kwargs)
            else:
                if fail_json:
                    return fail_json or {"error": "You are not logged in."}

        return inner

    return api_login_check_wrapper


def include_csrf(session_key: str = "csrf", form_key: str = "csrf", abort_code: int = 401):
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
                session[session_key] = Auth.generate_form_token()

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
