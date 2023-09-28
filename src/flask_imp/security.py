import typing as t
from functools import partial
from functools import wraps

from flask import abort
from flask import flash
from flask import redirect
from flask import request
from flask import session
from flask import url_for

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


def pass_function_check(
        function: t.Callable,
        predefined_args: t.Optional[t.Dict] = None,
        fail_endpoint: t.Optional[str] = None,
        pass_endpoint: t.Optional[str] = None,
        endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
        message: t.Optional[str] = None,
        message_category: str = "message",
        fail_on_missing_kwargs: bool = False,
        with_app_context: bool = False
):
    """
    A decorator that takes the result of a function and checks if it is True or False.

    URL variables from `@route` will be read by this decorator.
    To use URL variables in your passed in function,
    make sure your functions argument(s) name(s) match the name(s) of the URL variable(s).

    :raw-html:`<br />`

    **Example:**

    :raw-html:`<br />`

    .. code-block::

        def check_if_number(value):
            if isinstance(value, int):
                return True
            return False

        @bp.route("/admin-page/<int:value>", methods=["GET"])
        @login_check('logged_in', True, 'blueprint.login_page')  # can be mixed with login_check
        @pass_function_check(
            check_if_number,
            predefined_args=None,
            fail_endpoint='www.index',
            message="Failed message"
        )
        def admin_page():
            ...

        @bp.route("/admin-page/<int:value>", methods=["GET"])
        @login_check('logged_in', True, 'blueprint.login_page')  # can be mixed with login_check
        @pass_function_check(
            check_if_number,
            predefined_args={'value': 10},
            fail_endpoint='www.index',
            message="Failed message"
        )
        def admin_page_overwrite():
            ...

    :raw-html:`<br />`

    **Advanced use case:**

    Here's an example of accessing flask.session from within the passed in function. including the
    `with_app_context` parameter, the function will be called with `app_context()`.

    :raw-html:`<br />`

    .. code-block::

        from flask import current_app
        from flask import session

        ...

        def check_if_number(number=1, session_=None):
            if session_:
                print(session_)
            try:
                int(number)
                return True
            except ValueError:
                return False

        @bp.route("/pass-func-check-with-url-var/<number>", methods=["GET"])
        @pass_function_check(
            check_if_number,
            predefined_args={'number': 10, 'session_': session},
            fail_endpoint="www.index",
            with_app_context=True
        )
        def admin_page_overwrite_with_session():
            ...

    :raw-html:`<br />`

    If you pass in a predefined arg that has the same key name as a session variable that exists, the value
    of that predefined arg will be replaced with the session variable value.

    :raw-html:`<br />`

    .. code-block::

        session['car'] = 'Toyota'
        ...
        def check_function(car):
            if car == 'Toyota':
                return True
            return False
        ...
        @bp.route("/pass-func-check-with-url-var/<number>", methods=["GET"])
        @pass_function_check(
            check_function,
            predefined_args={'car': session},
            ...

        This will pass, as pass_function_check will replace the value of the predefined arg 'car' with the value
        of the session variable 'car'.

    :raw-html:`<br />`

    -----

    :param function: The function to call (this will be passed the url variables of the route.
    :param predefined_args: A dictionary of predefined arguments to pass to the function. Any keys that match any URL
                            variables will overwrite the URL variable specified in @route.
    :param fail_endpoint: The endpoint to redirect to if the
                          session key does not exist or does not contain the
                          specified values.
    :param pass_endpoint: The endpoint to redirect to if the function check passes.
    :param endpoint_kwargs: A dictionary of keyword arguments to pass to the redirect endpoint.
    :param message: If a message is specified, a flash message is shown.
    :param message_category: The category of the flash message.
    :param fail_on_missing_kwargs: If any of the required arguments for the passed in function are missing
                                    from the url variables, force function result to False.
    :param with_app_context: If True, the passed in function will be called with app_context().
    :return: The decorated function, or abort(403).
    """
    import inspect
    from flask import current_app
    from flask.sessions import SessionMixin

    def pass_function_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):

            def setup_flash(_message, _message_category):
                if _message:
                    partial_flash = partial(flash, _message)
                    if _message_category:
                        partial_flash(_message_category)
                    else:
                        partial_flash()

            function_args = dict(inspect.signature(function).parameters)
            passed_in_kwargs = {k: v for k, v in kwargs.items() if k in function_args}

            if predefined_args:

                passed_in_kwargs.update(predefined_args)

                for key, value in passed_in_kwargs.items():
                    if isinstance(value, SessionMixin):
                        if with_app_context:
                            with current_app.app_context():
                                if key in value:
                                    passed_in_kwargs[key] = value.get(key)

            try:
                if with_app_context:
                    with current_app.app_context():
                        func_result = True if function(**passed_in_kwargs) else False
                else:
                    func_result = True if function(**passed_in_kwargs) else False

            except TypeError:
                if fail_on_missing_kwargs:
                    func_result = False
                else:
                    return func(*args, **kwargs)

            if func_result:
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

            return abort(403)

        return inner

    return pass_function_wrapper


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
