import typing as t
from functools import partial
from functools import wraps
from inspect import signature

from flask import abort, session
from flask import redirect

from .._utilities import setup_flash, LazySession


def checkpoint_callable(
    callable_: t.Callable[..., t.Any],
    predefined_args: t.Optional[t.Dict[str, t.Any]] = None,
    include_url_args: bool = False,
    fail_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
    fail_json: t.Optional[t.Dict[str, t.Any]] = None,
    fail_status: int = 403,
    pass_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message",
) -> t.Callable[..., t.Any]:
    """
    A decorator that evaluates if the passed in callable is truly.

    Useful for feature flags or other checks that need to be done before a route is accessed.

    If `include_url_args` is set, the url variables of the route will be passed
    into the callable as `__url_vars__` after any predefined_args.

    *Example of using predefined_args*::

        def check_if_number(value):
            if isinstance(value, int):
                if value > 10:
                    return True
            return False

        @bp.route("/number", methods=["GET"])
        @checkpoint_callable(
            check_if_number,
            predefined_args={"value": os.getenv("NUMBER")},
            fail_url=lazy_url_for("www.index"),
            message="Failed message"
        )
        def number():
            ...

    *Example of checking route variable*::

        def check_url_vars(__url_vars__):
            if __url_vars__["value"] == 10:
                return True
            return False

        ...

        @bp.route("/number/<int:value>", methods=["GET"])
        @checkpoint_callable(
            check_url_vars,
            include_url_args=True,
            fail_url=lazy_url_for("wrong_number"),
            message="Failed message"
        )
        def number():
            ...

    *Example of using predefined_args from session*::

        def check_session_vars(value):
            # lazy_session_get is evaluated in the decorator.
            if value == 10:
                return True
            return False

        ...

        @bp.route("/number", methods=["GET"])
        @checkpoint_callable(
            check_session_vars,
            predefined_args={"value": lazy_session_get("NUMBER")},
            fail_url=lazy_url_for("www.index"),
            message="Failed message"
        )
        def number():
            ...

    :param callable_: the callable to call this will be passed the url variables of the route
    :param predefined_args: a dictionary of predefined arguments to pass to the callable
    :param include_url_args: load the url variables into the callable's arguments as __url_vars__
    :param fail_url: the url to redirect to if the callable fails
    :param fail_json: JSON that is returned on failure
    :param fail_status: the status code to abort with if the callable check fails
    :param pass_url: the url to redirect to if the callable passes
    :param message: if a message is specified, a flash message is shown
    :param message_category: the category of the flash message
    :return: the decorated callable, or abort(abort_status) response
    """

    def checkpoint_callable_wrapper(func: t.Any) -> t.Callable[..., t.Any]:
        @wraps(func)
        def inner(*args: t.Any, **kwargs: t.Any) -> t.Any:
            setup_flash(message, message_category)

            evaluated_predefined_args = {}

            if predefined_args:
                for k, v in predefined_args.items():
                    if isinstance(v, LazySession):
                        evaluated_predefined_args[k] = session.get(v.key, v.default)
                        continue

                    evaluated_predefined_args[k] = v

            if include_url_args:
                function_args = dict(signature(func).parameters)
                evaluated_predefined_args["__url_vars__"] = {
                    k: v for k, v in kwargs.items() if k in function_args
                }

            # evaluate callable
            if callable_(**evaluated_predefined_args):
                if pass_url:
                    setup_flash(message, message_category)

                    if isinstance(pass_url, str):
                        return redirect(pass_url)

                    if isinstance(pass_url, partial):
                        return redirect(pass_url())

                    raise TypeError("Pass URL must either be a string or a partial")

                return func(*args, **kwargs)

            #
            # Must have failed to get here
            #

            # If fail_json, return the fail_json
            if fail_json:
                return fail_json, fail_status

            # If fail_url is set, redirect to it
            if fail_url:
                setup_flash(message, message_category)

                if isinstance(fail_url, str):
                    return redirect(fail_url)

                if isinstance(fail_url, partial):
                    return redirect(fail_url())

                raise TypeError("Pass URL must either be a string or a partial")

            return abort(fail_status)

        return inner

    return checkpoint_callable_wrapper
