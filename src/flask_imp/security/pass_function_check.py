import typing as t
from functools import partial
from functools import wraps

from flask import abort
from flask import flash
from flask import redirect
from flask import url_for


def pass_function_check(
    function: t.Callable,
    predefined_args: t.Optional[t.Dict] = None,
    fail_endpoint: t.Optional[str] = None,
    pass_endpoint: t.Optional[str] = None,
    endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message",
    fail_on_missing_kwargs: bool = False,
    with_app_context: bool = False,
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
