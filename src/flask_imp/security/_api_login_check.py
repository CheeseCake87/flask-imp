import typing as t
from functools import wraps

from ._private_funcs import _check_against_values_allowed


def api_login_check(
    session_key: str,
    values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
    fail_json: t.Optional[t.Dict[str, t.Any]] = None,
    fail_status: int = 401,
) -> t.Callable[..., t.Any]:
    """
    A decorator that is used to secure API routes using the session.

    Example of a route that requires a user to be logged in::

        @bp.route("/api/resource", methods=["GET"])
        @api_login_check('logged_in', True)
        def api_page():
            ...

    You can also supply your own failed return JSON::

        @bp.route("/api/resource", methods=["GET"])
        @api_login_check('logged_in', True, fail_json={"error": "You are not logged in."})
        def api_page():
            ...

    **Note:** Using this on a route will require you to include credentials on the request.

    Here's an example using JavaScript fetch()::

        fetch("/api/resource", {
            method: "GET",
            credentials: "include"
        })

    :param session_key: the session key to check for
    :param values_allowed: a list of or singular value(s) that the session key must contain
    :param fail_json: JSON that is returned on failure - defaults to {"error": "You are not logged in."}
    :param fail_status: the status code to return on failure - defaults to 401
    :return: the decorated function, or a JSON fail response
    """
    from flask import session

    def api_login_check_wrapper(func: t.Any) -> t.Callable[..., t.Any]:
        @wraps(func)
        def inner(*args: t.Any, **kwargs: t.Any) -> t.Any:
            skey = session.get(session_key)
            if skey is not None:
                if _check_against_values_allowed(skey, values_allowed):
                    return func(*args, **kwargs)

            return fail_json, fail_status

        return inner

    return api_login_check_wrapper
