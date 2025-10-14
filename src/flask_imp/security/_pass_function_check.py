import typing as t
from functools import partial
from functools import wraps

from flask import abort
from flask import flash
from flask import redirect


def pass_function_check(
    function: t.Callable[..., t.Any],
    predefined_args: t.Optional[t.Dict[str, t.Any]] = None,
    pass_url: t.Optional[t.Union[str | partial]] = None,
    fail_url: t.Optional[t.Union[str | partial]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message",
    fail_on_missing_kwargs: bool = False,
    abort_status: int = 403,
) -> t.Callable[..., t.Any]:
    """
    A decorator that takes the result of a function and checks if it is True or False.

    Useful for feature flags or other checks that need to be done before a route is accessed.

    URL variables from `@route` will be read by this decorator.
    To use URL variables in your passed in function,
    make sure your functions argument(s) name(s) match the name(s) of the URL variable(s).

    *Example function*::

        def check_if_number(value):
            if isinstance(value, int):
                if value > 10:
                    return True
            return False

    *Example of checking route variable*::

        @bp.route("/number/<int:value>", methods=["GET"])
        @pass_function_check(
            check_if_number,
            fail_url=lazy_url_for("wrong_number"),
            message="Failed message"
        )
        def number():
            ...

    *Example of using predefined_args*::

        @bp.route("/number", methods=["GET"])
        @pass_function_check(
            check_if_number,
            predefined_args={"value": os.getenv("NUMBER")},
            fail_url=lazy_url_for("www.index"),
            message="Failed message"
        )
        def number():
            ...

    :param function: the function to call this will be passed the url variables of the route
    :param predefined_args: a dictionary of predefined arguments to pass to the
                            function. Any keys that match any URL
                            variables will overwrite the URL variable
                            specified in @route
    :param pass_url: the url to redirect to if the function passes
    :param fail_url: the url to redirect to if the function fails
    :param message: if a message is specified, a flash message is shown
    :param message_category: the category of the flash message
    :param fail_on_missing_kwargs: if any of the required arguments for the passed in function are missing
                                    from the url variables, force function result to False
    :param abort_status: the status code to abort with if the function check fails
    :return: the decorated function, or abort(abort_status) response
    """
    import inspect
    from flask.sessions import SessionMixin

    def pass_function_wrapper(func: t.Any) -> t.Callable[..., t.Any]:
        @wraps(func)
        def inner(*args: t.Any, **kwargs: t.Any) -> t.Any:
            def setup_flash(
                _message: t.Optional[str], _message_category: t.Optional[str]
            ) -> None:
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
                        if key in value:
                            passed_in_kwargs[key] = value.get(key)

            try:
                func_result = True if function(**passed_in_kwargs) else False

            except TypeError:
                if fail_on_missing_kwargs:
                    func_result = False
                else:
                    return func(*args, **kwargs)

            if func_result:
                if pass_url:
                    setup_flash(message, message_category)

                    if isinstance(pass_url, str):
                        return redirect(pass_url)

                    if isinstance(pass_url, partial):
                        return redirect(pass_url())

                    raise TypeError("Pass URL must either be a string or a partial")

                return func(*args, **kwargs)

            if fail_url:
                setup_flash(message, message_category)

                if isinstance(fail_url, str):
                    return redirect(fail_url)

                if isinstance(fail_url, partial):
                    return redirect(fail_url())

                raise TypeError("Pass URL must either be a string or a partial")

            return abort(abort_status)

        return inner

    return pass_function_wrapper
