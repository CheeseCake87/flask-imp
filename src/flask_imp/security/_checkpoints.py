"""
Basic:
{
    "auth.parameters": {
        "password": "pass",
        "username": "user"
    },
    "auth.token": null,
    "auth.type": "basic"
}

Bearer:
{
    "auth.parameters": {},
    "auth.token": "hello",
    "auth.type": "bearer"
}

"""

import typing as t

from flask import request
from flask import session

from .._utilities import check_against_values_allowed


class BaseCheckpoint:
    """
    Must never be instantiated directly.
    """

    pass_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None
    fail_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None
    fail_json: t.Optional[t.Dict[str, t.Any]] = None
    fail_status: int = 403
    message: t.Optional[str] = None
    message_category: str = "message"

    def action(
        self,
        fail_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
        fail_json: t.Optional[t.Dict[str, t.Any]] = None,
        fail_status: int = 403,
        pass_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
        message: t.Optional[str] = None,
        message_category: str = "message",
    ) -> "BaseCheckpoint":
        """
        Set the actions to take for this checkpoint.

        If fail_json is provided, passing to endpoints will be disabled.

        `pass_url` and `fail_url` take either a string or the `utilities.lazy_url_for` function.

        Here's an example of `lazy_url_for` usage::

            from flask_imp.utilities import lazy_url_for

            CHECKPOINT = ...(...).action(pass_url=lazy_url_for(endpoint))

            @app.get("/protected")
            @checkpoint(CHECKPOINT)
            ..

        ---

        :param fail_url: the url to redirect to if the key value fails
        :param fail_json: JSON that is returned on failure
        :param fail_status: the status code to return if the check fails
        :param pass_url: the url to redirect to if the key value passes
        :param message: a message to add to Flask's flash
        :param message_category: the category of the flash message
        """
        self.pass_url = pass_url
        self.fail_url = fail_url
        self.fail_json = fail_json
        self.fail_status = fail_status
        self.message = message
        self.message_category = message_category

        return self

    def pass_(self) -> bool:
        raise NotImplementedError()


class APIKeyCheckpoint(BaseCheckpoint):
    key: str
    header: str
    type_: t.Literal["header", "query_param"]

    def __init__(
        self,
        key: str,
        type_: t.Literal["header", "query_param"] = "header",
        header_or_param: str = "x-api-key",
    ):
        """
        A checkpoint that checks if the specified header or query parameter exists,
        and that the key in the request is valid.

        Note: Query parameters are case-sensitive.

        :param key: the key to validate against
        :param type_: where to look for the key
        :param header_or_param: what header or query param value will the key be expected
        """
        self.key = key
        self.type_ = type_
        self.header_or_param = header_or_param

    def pass_(self) -> bool:
        if self.type_ == "header":
            if header_value := request.headers.get(self.header_or_param):
                if header_value == self.key:
                    return True

        if self.type_ == "query_param":
            # Query Params are case-sensitive :(
            if query_param_value := request.args.get(self.header_or_param):
                if query_param_value == self.key:
                    return True

        return False


class BearerCheckpoint(BaseCheckpoint):
    token: str

    def __init__(
        self,
        token: str,
    ):
        """
        A checkpoint that checks if the authorization header is of type Bearer,
        and that the token in the request is valid.

        :param token: the token to check for
        """
        self.token = token

    def pass_(self) -> bool:
        if auth := request.authorization:
            if auth.type == "bearer" and auth.token == self.token:
                return True

        return False


class SessionCheckpoint(BaseCheckpoint):
    session_key: str
    values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool]

    def __init__(
        self,
        session_key: str,
        values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
    ):
        """
        A checkpoint that checks if the specified session key exists and its value(s) match the specified value(s).

        :param session_key: the session key to check for
        :param values_allowed: a list of or singular value(s) that the session key must contain
        """
        self.session_key = session_key
        self.values_allowed = values_allowed

    def pass_(self) -> bool:
        value = session.get(self.session_key)
        if check_against_values_allowed(value, self.values_allowed):
            return True

        return False


__all__ = [
    "BaseCheckpoint",
    "APIKeyCheckpoint",
    "BearerCheckpoint",
    "SessionCheckpoint",
]
