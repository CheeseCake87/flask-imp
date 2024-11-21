import typing as t
from functools import partial
from functools import wraps

from flask import abort
from flask import flash
from flask import redirect
from flask import session
from flask import url_for

from ._private_funcs import _check_against_values_allowed


def login_check(
    session_key: str,
    values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
    fail_endpoint: t.Optional[str] = None,
    pass_endpoint: t.Optional[str] = None,
    endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message",
    abort_status: int = 403,
) -> t.Callable[..., t.Any]:
    """
    A decorator that checks if the specified session key exists and contains the specified value.

    Example of a route that requires a user to be logged in::

        @bp.route("/admin", methods=["GET"])
        @login_check(
            'logged_in',
            True,
            fail_endpoint='blueprint.login_page',
            message="Login needed"
        )
        def admin_page():
            ...

    Example of a route that if the user is already logged in, redirects to the specified endpoint::

        @bp.route("/login-page", methods=["GET"])
        @login_check(
            'logged_in',
            True,
            pass_endpoint='blueprint.admin_page',
            message="Already logged in"
        )
        def login_page():
            ...

    :param session_key: the session key to check for
    :param values_allowed: a list of or singular value(s) that the session key must contain
    :param fail_endpoint: the endpoint to redirect to if the session key does not exist or
                          match the pass_value
    :param pass_endpoint: the endpoint to redirect to if the session key passes
                          Used to redirect away from login pages, if already logged in
    :param endpoint_kwargs: a dictionary of keyword arguments to pass to the redirect endpoint
    :param message: a message to add to flask.flash()
    :param message_category: the category of the flash message
    :param abort_status: the status code to abort with if the session key does not exist or match the pass_value
    :return: the decorated function, or abort(abort_code) response
    """

    def login_check_wrapper(func: t.Any) -> t.Callable[..., t.Any]:
        @wraps(func)
        def inner(*args: t.Any, **kwargs: t.Any) -> t.Any:
            skey = session.get(session_key)

            def setup_flash(
                _message: t.Optional[str], _message_category: t.Optional[str]
            ) -> None:
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
                        return redirect(
                            url_for(
                                fail_endpoint,
                                _anchor=None,
                                _method=None,
                                _scheme=None,
                                _external=None,
                                **endpoint_kwargs,
                            )
                        )

                    return redirect(url_for(fail_endpoint))

                return func(*args, **kwargs)

            if skey is not None:
                if _check_against_values_allowed(skey, values_allowed):
                    if pass_endpoint:
                        setup_flash(message, message_category)

                        if endpoint_kwargs:
                            return redirect(
                                url_for(
                                    pass_endpoint,
                                    _anchor=None,
                                    _method=None,
                                    _scheme=None,
                                    _external=None,
                                    **endpoint_kwargs,
                                )
                            )

                        return redirect(url_for(pass_endpoint))

                    return func(*args, **kwargs)

                if fail_endpoint:
                    setup_flash(message, message_category)

                    if endpoint_kwargs:
                        return redirect(
                            url_for(
                                fail_endpoint,
                                _anchor=None,
                                _method=None,
                                _scheme=None,
                                _external=None,
                                **endpoint_kwargs,
                            )
                        )

                    return redirect(url_for(fail_endpoint))

                return func(*args, **kwargs)

            return abort(abort_status)

        return inner

    return login_check_wrapper
