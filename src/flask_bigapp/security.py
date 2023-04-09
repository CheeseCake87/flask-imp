import typing as t
from functools import wraps

from flask import flash
from flask import redirect
from flask import session
from flask import url_for


def login_check(
        bool_session_key: str,
        endpoint_redirect: str,
        redirect_on_value: bool = False,
        endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
        message: t.Optional[str] = None,
        message_category: str = "message"
):
    """
    A decorator that checks if the specified session key exists, redirects to the specified endpoint if it does not
    exist or match the specified value.

    Example of a route that requires a user to be logged in:

    @bp.route("/admin", methods=["GET"])
    @login_check('logged_in', 'blueprint.login_page', message="Login needed")
    def admin_page():
        ...

    Example of a route that if the user is already logged in, redirects to the specified endpoint:

    @bp.route("/login-page", methods=["GET"])
    @login_check('logged_in', 'blueprint.admin_page', redirect_on_value=True, message="Already logged in")
    def login_page():
        ...

    :param bool_session_key: The session key to check for.
    :param endpoint_redirect: The endpoint to redirect to
                              if the session key does not exist or
                              match the specified value.
    :param redirect_on_value: The boolean value to check the session key against.
    :param endpoint_kwargs: A dictionary of keyword arguments to pass to the redirect endpoint.
    :param message: If a message is specified, a flash message is shown.
    :param message_category: The category of the flash message.
    """

    def login_check_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if bool_session_key not in session:
                if message:
                    flash(message, message_category)
                if endpoint_kwargs is None:
                    return redirect(url_for(endpoint_redirect))
                return redirect(url_for(endpoint_redirect, **endpoint_kwargs))

            if session[bool_session_key] == redirect_on_value:
                if message:
                    flash(message, message_category)
                if endpoint_kwargs is None:
                    return redirect(url_for(endpoint_redirect))
                return redirect(url_for(endpoint_redirect, **endpoint_kwargs))

            return func(*args, **kwargs)

        return inner

    return login_check_wrapper


def permission_check(
        iter_session_key: str,
        endpoint_redirect: str,
        redirect_if_no_match: t.Optional[list] = None,
        endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
        message: t.Optional[str] = None,
        message_category: str = "message"
):
    """
    A decorator that checks if the specified session key exists, redirects to the specified endpoint if
    the session key does not exist or if the session key does not contain the specified values.

    Example:

    @bp.route("/admin-page", methods=["GET"])
    @login_check('logged_in', 'blueprint.login_page') <- can be mixed with login_check
    @permission_check('permissions', 'www.index', redirect_if_no_match=['admin'],
                      message="You don't have the correct permissions to view this page.")
    def admin_page():
        ...

    IF redirect_if_no_match is None, the default value of ['admin'] is set.

    :param iter_session_key: The session key to check for.
    :param endpoint_redirect: The endpoint to redirect to if the
                              session key does not exist or does not contain the
                              specified values.
    :param redirect_if_no_match: A list of values that the session key must contain.
    :param endpoint_kwargs: A dictionary of keyword arguments to pass to the redirect endpoint.
    :param message: If a message is specified, a flash message is shown.
    :param message_category: The category of the flash message.
    """

    if redirect_if_no_match is None:
        redirect_if_no_match = ['admin']

    def permission_check_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if iter_session_key not in session:
                if message:
                    flash(message, message_category)
                if endpoint_kwargs is None:
                    return redirect(url_for(endpoint_redirect))
                return redirect(url_for(endpoint_redirect, **endpoint_kwargs))

            for item in redirect_if_no_match:
                if item not in session[iter_session_key]:
                    if message:
                        flash(message, message_category)
                    if endpoint_kwargs is None:
                        return redirect(url_for(endpoint_redirect))
                    return redirect(url_for(endpoint_redirect, **endpoint_kwargs))

            return func(*args, **kwargs)

        return inner

    return permission_check_wrapper


class BigAppSecurity:
    """
    A class that provides route function decorators to check for session variables and their values.
    """

    @staticmethod
    def login_required(
            redirect_endpoint: str,
            bool_key_name: str,
            show_message: bool = True,
            message: str = "You need to be logged in to access this page."
    ):

        def login_required_wrapper(func):
            @wraps(func)
            def secure_function(*args, **kwargs):
                if bool_key_name not in session:
                    if show_message:
                        flash(message)
                    return redirect(url_for(redirect_endpoint))

                if not session[bool_key_name]:
                    if show_message:
                        flash(message)
                    return redirect(url_for(redirect_endpoint))

                return func(*args, **kwargs)

            return secure_function

        return login_required_wrapper

    @staticmethod
    def no_login_required(
            redirect_endpoint: str,
            session_bool_key_name: str,
            show_message: bool = True,
            message: str = "You are already logged in."
    ):

        def no_login_required_wrapper(func):
            @wraps(func)
            def secure_function(*args, **kwargs):
                if session_bool_key_name in session:
                    if session[session_bool_key_name]:
                        if show_message:
                            flash(message)
                        return redirect(url_for(redirect_endpoint))

                return func(*args, **kwargs)

            return secure_function

        return no_login_required_wrapper

    @staticmethod
    def permission_required(
            redirect_endpoint: str,
            session_list_key: str,
            permission_needed: str,
            show_message: bool = True,
            message: str = "You don't have the required permissions to access this page."
    ):

        def permission_required(func):
            @wraps(func)
            def secure_function(*args, **kwargs):
                if session_list_key not in session:
                    if show_message:
                        flash(message)
                    return redirect(url_for(redirect_endpoint))

                if permission_needed not in session[session_list_key]:
                    if show_message:
                        flash(message)
                    return redirect(url_for(redirect_endpoint))

                return func(*args, **kwargs)

            return secure_function

        return permission_required
