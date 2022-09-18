from functools import wraps
from flask import redirect
from flask import flash
from flask import session
from flask import url_for


class BigAppSecurity:
    """
    A class that provides route function decorators to check for session variables and their values.
    """

    @staticmethod
    def login_required(
            redirect_endpoint: str,
            bool_key_name: str,
            show_message: bool = True,
            message: str = None
    ):
        if message is None:
            message = "You need to be logged in to access this page."

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
            message: str = None
    ):
        if message is None:
            message = "You are already logged in."

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
            message: str = None
    ):
        if message is None:
            message = "You don't have the required permissions to access this page."

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
