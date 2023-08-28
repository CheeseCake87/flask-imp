import typing as t
from functools import wraps

from flask import flash
from flask import redirect
from flask import session
from flask import url_for


def login_check(
        session_key: str,
        pass_value: t.Union[bool, str, int],
        fail_endpoint: str,
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
    :param pass_value: Set the value that the session key must contain to pass the check.
                       It can be a boolean, string or integer.
    :param fail_endpoint: The endpoint to redirect to if the session key does not exist or
                          match the pass_value.
    :param endpoint_kwargs: A dictionary of keyword arguments to pass to the redirect endpoint.
    :param message: If a message is specified, a flash message is shown.
    :param message_category: The category of the flash message.
    """

    def login_check_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            skey = session.get(session_key)
            if skey:
                if skey == pass_value:
                    return func(*args, **kwargs)

            if message:
                flash(message, message_category)

            if endpoint_kwargs:
                return redirect(url_for(fail_endpoint, **endpoint_kwargs))

            return redirect(url_for(fail_endpoint))

        return inner

    return login_check_wrapper


def api_login_check(
        session_key: str,
        pass_value: t.Union[bool, str, int],
        fail_json: t.Optional[t.Dict[str, t.Any]] = None
):
    """
    A decorator that checks if the specified session key exists shows a 401 error if it does not

    Example of a route that requires a user to be logged in:

    @bp.route("/api/resource", methods=["GET"])
    @api_login_check('logged_in')
    def api_page():
        ...

    You can also supply your own failed return JSON:

    @bp.route("/api/resource", methods=["GET"])
    @api_login_check('logged_in', json_to_return={"error": "You are not logged in."})
    def api_page():
        ...

    Default json_to_return is {"error": "You are not logged in."}

    :param session_key: The session key to check for.
    :param pass_value: Set the value that the session key must contain to pass the check. Can be a boolean, string or
                       integer.
    :param fail_json: JSON that is returned on failure.
    """

    def api_login_check_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            skey = session.get(session_key)
            if skey:
                if skey == pass_value:
                    return func(*args, **kwargs)
            else:
                if fail_json:
                    return fail_json or {"error": "You are not logged in."}

        return inner

    return api_login_check_wrapper


def permission_check(
        session_key: str,
        values_allowed: t.Union[list[str, int, bool], str, int, bool],
        fail_endpoint: str,
        endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
        message: t.Optional[str] = None,
        message_category: str = "message"
):
    """
    A decorator that checks if the specified session key exists redirects to the specified endpoint if
    the session key does not exist or if the session key does not contain the specified values.

    Example:

    @bp.route("/admin-page", methods=["GET"])
    @login_check('logged_in', 'blueprint.login_page') <- can be mixed with login_check
    @permission_check('permissions', ['admin'], 'www.index',
                      message="You don't have the correct permissions to view this page.")
    def admin_page():
        ...

    IF redirect_if_no_match is None, the default value of ['admin'] is set.

    :param session_key: The session key to check for.
    :param values_allowed: A list of values that the session key must contain.
    :param fail_endpoint: The endpoint to redirect to if the
                              session key does not exist or does not contain the
                              specified values.
    :param endpoint_kwargs: A dictionary of keyword arguments to pass to the redirect endpoint.
    :param message: If a message is specified, a flash message is shown.
    :param message_category: The category of the flash message.
    """

    def permission_check_wrapper(func):

        def check_against_values_allowed(this_value: t.Union[list, str, int, bool]) -> bool:
            if isinstance(values_allowed, list):
                if this_value in values_allowed:
                    return True
                return False

            if this_value == values_allowed:
                return True

            return False

        @wraps(func)
        def inner(*args, **kwargs):
            skey = session.get(session_key)

            if skey:
                if isinstance(skey, list):
                    for value in skey:
                        if check_against_values_allowed(value):
                            return func(*args, **kwargs)

                if check_against_values_allowed(skey):
                    return func(*args, **kwargs)

            if message:
                flash(message, message_category)

            if endpoint_kwargs:
                return redirect(url_for(fail_endpoint, **endpoint_kwargs))

            return redirect(url_for(fail_endpoint))

        return inner

    return permission_check_wrapper
