import typing as t
from functools import partial
from functools import wraps

from flask import abort
from flask import flash
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from ._checkpoints import (
    AuthorizationBearerCheckpoint,
    SessionCheckpoint,
)
from ._private_funcs import _check_against_values_allowed


def checkpoint(
    checkpoint_: SessionCheckpoint | AuthorizationBearerCheckpoint,
) -> t.Callable[..., t.Any]:
    """
    A decorator that checks the specified Checkpoint class.

    NOTE: If the incoming request is JSON and no fail_json or endpoints
    are set, the decorator will return the following JSON on failure:

        {"error": "Unauthorized"}

    Example of a route that requires a user to be logged in::

        @bp.route("/admin", methods=["GET"])
        @checkpoint(
            SessionCheckpoint(
                'logged_in',
                True,
                fail_endpoint='blueprint.login_page',
                message="Login needed"
            )
        )
        def admin_page():
            ...

    Example of a route that if the user is already logged in, redirects to the specified endpoint::

        @bp.route("/login-page", methods=["GET"])
        @checkpoint(
            SessionCheckpoint(
                'logged_in',
                True,
                pass_endpoint='blueprint.admin_page',
                message="Already logged in"
            )
        )
        def login_page():
            ...

    Example of a route that requires a user to be logged in and to be an admin::

        @bp.route("/admin", methods=["GET"])
        @checkpoint(
            SessionCheckpoint(
                'logged_in',
                True,
                fail_endpoint='blueprint.login_page',
                message="Login needed"
            )
        )
        @checkpoint(
            SessionCheckpoint(
                'user_type',
                'admin',
                fail_endpoint='blueprint.index',
                message="You need to be an admin to access this page"
            )
        )
        def admin_page():
            ...

    You can also supply your own failed return JSON::

        @bp.route("/api/resource", methods=["GET"])
        @checkpoint(
            SessionCheckpoint(
                'logged_in',
                True,
                fail_json={"error": "You are not logged in."}
            )
        def api_page():
            ...

    **Note:** Using this on a API route will require you to include credentials on the request.

    Here's an example using JavaScript fetch()::

        fetch("/api/resource", {
            method: "GET",
            credentials: "include"
        })

    :return: the decorated function, or abort(fail_status), or redirect, or fail_json response
    """

    def checkpoint_wrapper(func: t.Any) -> t.Callable[..., t.Any]:
        @wraps(func)
        def inner(*args: t.Any, **kwargs: t.Any) -> t.Any:
            passing = False

            def setup_flash(
                _message: t.Optional[str], _message_category: t.Optional[str]
            ) -> None:
                if _message:
                    partial_flash = partial(flash, _message)
                    if _message_category:
                        partial_flash(_message_category)
                    else:
                        partial_flash()

            if isinstance(checkpoint_, SessionCheckpoint):
                skey = session.get(checkpoint_.session_key)
                if skey is not None:
                    if _check_against_values_allowed(skey, checkpoint_.values_allowed):
                        passing = True

            if isinstance(checkpoint_, AuthorizationBearerCheckpoint):
                auth = request.authorization
                if auth.type == "bearer" and auth.token == checkpoint_.token:
                    passing = True

            if passing:
                if not checkpoint_.fail_json:
                    if checkpoint_.pass_endpoint:
                        setup_flash(checkpoint_.message, checkpoint_.message_category)

                        if checkpoint_.endpoint_kwargs:
                            return redirect(
                                url_for(
                                    checkpoint_.pass_endpoint,
                                    _anchor=None,
                                    _method=None,
                                    _scheme=None,
                                    _external=None,
                                    **checkpoint_.endpoint_kwargs,
                                )
                            )

                        return redirect(url_for(checkpoint_.pass_endpoint))

                return func(*args, **kwargs)

            # Must have failed to get here

            # If fail_json, return the fail_json
            if checkpoint_.fail_json:
                return checkpoint_.fail_json, checkpoint_.fail_status

            # If fail_endpoint is set, redirect to it
            if checkpoint_.fail_endpoint:
                setup_flash(checkpoint_.message, checkpoint_.message_category)

                if checkpoint_.endpoint_kwargs:
                    return redirect(
                        url_for(
                            checkpoint_.fail_endpoint,
                            _anchor=None,
                            _method=None,
                            _scheme=None,
                            _external=None,
                            **checkpoint_.endpoint_kwargs,
                        )
                    )

                return redirect(url_for(checkpoint_.fail_endpoint))

            # if the request is JSON, return JSON
            if request.is_json:
                return {"error": "Unauthorized"}, checkpoint_.fail_status

            # Otherwise, abort with the specified status code
            return abort(checkpoint_.fail_status)

        return inner

    return checkpoint_wrapper
