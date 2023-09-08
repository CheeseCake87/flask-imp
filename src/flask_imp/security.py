import typing as t
from functools import wraps

from flask import flash, abort
from flask import redirect
from flask import session
from flask import url_for


def _check_against_values_allowed(
        session_value: t.Union[list, str, int, bool],
        values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
) -> bool:
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

    Example of a route that requires a user to be logged in:

    @bp.route("/admin", methods=["GET"])
    @login_check('logged_in', True, 'blueprint.login_page', message="Login needed")
    def admin_page():
        ...

    Example of a route that if the user is already logged in, redirects to the specified endpoint:

    @bp.route("/login-page", methods=["GET"])
    @login_check('logged_in', True, 'blueprint.admin_page', message="Already logged in")
    def login_page():
        ...

    :param session_key: The session key to check for.
    :param values_allowed: A list of or singular value(s) that the session key must contain.
    :param fail_endpoint: The endpoint to redirect to if the session key does not exist or
                          match the pass_value.
    :param pass_endpoint: The endpoint to redirect to if the session key passes.
                          Used to redirect away from login pages, if already logged in.
    :param endpoint_kwargs: A dictionary of keyword arguments to pass to the redirect endpoint.
    :param message: If a message is specified, a flash message is shown.
    :param message_category: The category of the flash message.
    """

    def login_check_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            skey = session.get(session_key)

            if skey is None:
                if fail_endpoint:
                    if endpoint_kwargs:
                        return redirect(url_for(fail_endpoint, **endpoint_kwargs))

                    return redirect(url_for(fail_endpoint))

                return func(*args, **kwargs)

            if skey is not None:
                if _check_against_values_allowed(skey, values_allowed):
                    if pass_endpoint:
                        if message:
                            flash(message, message_category)

                        if endpoint_kwargs:
                            return redirect(url_for(pass_endpoint, **endpoint_kwargs))

                        return redirect(url_for(pass_endpoint))

                    return func(*args, **kwargs)

                if fail_endpoint:
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

    Example:

    @bp.route("/admin-page", methods=["GET"])
    @login_check('logged_in', 'blueprint.login_page') <- can be mixed with login_check
    @permission_check('permissions', ['admin'], 'www.index', message="Failed message", message_category="error")
    def admin_page():
        ...

    :param session_key: The session key to check for.
    :param values_allowed: A list of or singular value(s) that the session key must contain.
    :param fail_endpoint: The endpoint to redirect to if the
                          session key does not exist or does not contain the
                          specified values.
    :param endpoint_kwargs: A dictionary of keyword arguments to pass to the redirect endpoint.
    :param message: If a message is specified, a flash message is shown.
    :param message_category: The category of the flash message.
    """

    def permission_check_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            skey = session.get(session_key)

            if skey:
                if _check_against_values_allowed(skey, values_allowed):
                    return func(*args, **kwargs)

            if message:
                flash(message, message_category)

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
    A decorator that is used to secure API routes that return a JSON response.

    Example of a route that requires a user to be logged in:

    @bp.route("/api/resource", methods=["GET"])
    @api_login_check('logged_in', True)
    def api_page():
        ...


    You can also supply your own failed return JSON:

    @bp.route("/api/resource", methods=["GET"])
    @api_login_check('logged_in', True, fail_json={"error": "You are not logged in."})
    def api_page():
        ...


    Default json_to_return is {"error": "You are not logged in."}

    :param session_key: The session key to check for.
    :param values_allowed: A list of or singular value(s) that the session key must contain.
    :param fail_json: JSON that is returned on failure.
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
