import typing as t
from functools import partial
from functools import wraps

from flask import abort
from flask import flash
from flask import redirect
from flask import session
from flask import url_for

from .__private_funcs__ import _check_against_values_allowed


def permission_check(
    session_key: str,
    values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
    fail_endpoint: t.Optional[str] = None,
    endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message",
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
