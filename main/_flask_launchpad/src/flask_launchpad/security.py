from functools import wraps
from flask import redirect
from flask import flash
from flask import session
from flask import url_for


class Security:
    """
    A class that provides route function decorators to check for session variables and their values.
    """

    _app = None

    def __init__(self, app=None):
        """
        init method, fires init_app if app name is passed in. This is usually used when NOT using create_app()
        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        """
        init method used when working with create_app()
        """
        if app is None:
            raise ImportError("No app passed into the FlaskLaunchpad app")
        self._app = app

    def login_required(
            self,
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
                with self._app.app_context():
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

    def no_login_required(
            self,
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
                with self._app.app_context():
                    if session_bool_key_name in session:
                        if session[session_bool_key_name]:
                            if show_message:
                                flash(message)
                            return redirect(url_for(redirect_endpoint))

                return func(*args, **kwargs)

            return secure_function

        return no_login_required_wrapper

    def permission_required(
            self,
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
                with self._app.app_context():
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
