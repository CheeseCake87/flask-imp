import typing as t
from functools import partial
from functools import wraps

from flask import abort
from flask import redirect
from flask import request

from ._checkpoints import (
    BaseCheckpoint,
    APIKeyCheckpoint,
    BearerCheckpoint,
    SessionCheckpoint,
)
from .._utilities import setup_flash

AnyCheckpoint = t.Union[APIKeyCheckpoint, BearerCheckpoint, SessionCheckpoint]


def checkpoint(checkpoint_: AnyCheckpoint) -> t.Callable[..., t.Any]:
    """
    A decorator that checks the specified Checkpoint class.

    NOTE: If the incoming request is JSON and no fail_json or endpoints
    are set, the decorator will return the following JSON on failure:

        {"error": "Unauthorized"}

    Example of a route that requires a user to be logged in::

        LOGIN_REQUIRED = SessionCheckpoint(
            'logged_in', True
        ).action(
            lazy_url_for('blueprint.login_page')
        )

        @bp.route("/admin", methods=["GET"])
        @checkpoint(LOGIN_REQUIRED)
        def admin_page():
            ...

    Example of a route that if the user is already logged in, redirects to the specified endpoint::

        IS_LOGGED_IN = SessionCheckpoint(
            'logged_in', True
        ).action(
            pass_url=lazy_url_for('blueprint.admin_page'),
            message="Already logged in"
        )

        @bp.route("/login-page", methods=["GET"])
        @checkpoint(IS_LOGGED_IN)
        def login_page():
            ...

    Example of a route that requires a user to be logged in and to be an admin::

        LOGIN_REQUIRED = SessionCheckpoint(
            session_key="logged_in",
            values_allowed=True,
        ).action(
            fail_url=lazy_url_for("blueprint.login_page"),
        )

        PERM_REQUIRED = SessionCheckpoint(
            session_key="user_type",
            values_allowed="admin",
        ).action(
            fail_url=lazy_url_for("blueprint.index"),
            message="You need to be an admin to access this page"
        )

        @bp.route("/admin", methods=["GET"])
        @checkpoint(LOGIN_REQUIRED)
        @checkpoint(PERM_REQUIRED)
        def admin_page():
            ...

    You can also supply your own failed return JSON::

        JS_FETCH_CHECKPOINT = SessionCheckpoint(
            'logged_in', True
        ).action(
            fail_json={"error": "You are not logged in."}
        )

        @bp.route("/api/resource", methods=["GET"])
        @checkpoint(JS_FETCH_CHECKPOINT)
        def api_page():
            ...

    **Note:** Using this on a API route will require you to include credentials on the request.

    Here's an example using JavaScript fetch()::

        fetch("/api/resource", {
            method: "GET",
            credentials: "include"
        })...

    :param checkpoint_: the checkpoint class to pass or fail
    :return: the decorated function, or abort(fail_status), or redirect, or fail_json response
    """

    def checkpoint_wrapper(func: t.Any) -> t.Callable[..., t.Any]:
        @wraps(func)
        def inner(*args: t.Any, **kwargs: t.Any) -> t.Any:
            if not isinstance(checkpoint_, BaseCheckpoint):
                raise TypeError("Must be an instance of a Checkpoint")

            if checkpoint_.pass_():
                if not checkpoint_.fail_json:
                    if checkpoint_.pass_url:
                        setup_flash(checkpoint_.message, checkpoint_.message_category)

                        if isinstance(checkpoint_.pass_url, str):
                            return redirect(checkpoint_.pass_url)

                        if isinstance(checkpoint_.pass_url, partial):
                            return redirect(checkpoint_.pass_url())

                        raise TypeError("Pass URL must either be a string or a partial")

                return func(*args, **kwargs)

            #
            # Must have failed to get here
            #

            # If fail_json, return the fail_json
            if checkpoint_.fail_json:
                return checkpoint_.fail_json, checkpoint_.fail_status

            # If fail_url is set, redirect to it
            if checkpoint_.fail_url:
                setup_flash(checkpoint_.message, checkpoint_.message_category)

                if isinstance(checkpoint_.fail_url, str):
                    return redirect(checkpoint_.fail_url)

                if isinstance(checkpoint_.fail_url, partial):
                    return redirect(checkpoint_.fail_url())

                raise TypeError("Fail URL must either be a string or a partial")

            # if the request is JSON, return JSON
            if request.is_json:
                return {"error": "Unauthorized"}, checkpoint_.fail_status

            # Otherwise, abort with the specified status code
            return abort(checkpoint_.fail_status)

        return inner

    return checkpoint_wrapper
