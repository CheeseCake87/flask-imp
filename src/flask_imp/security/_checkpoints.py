import typing as t


class AuthorizationBearerCheckpoint:
    token: str
    pass_endpoint: t.Optional[str]
    fail_endpoint: t.Optional[str]
    endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]]
    fail_json: t.Optional[t.Dict[str, t.Any]]
    fail_status: int
    message: t.Optional[str]
    message_category: str

    def __init__(
        self,
        token: str,
        pass_endpoint: t.Optional[str] = None,
        fail_endpoint: t.Optional[str] = None,
        endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
        fail_json: t.Optional[t.Dict[str, t.Any]] = None,
        fail_status: int = 403,
        message: t.Optional[str] = None,
        message_category: str = "message",
    ):
        """
        A checkpoint that checks if the Authorization header is set to a valid token.

        If fail_json is provided, passing to endpoints will be disabled.

        :param token: the token to check for
        :param fail_endpoint: the endpoint to redirect to if the session key does not exist or
                              match the pass_value
        :param pass_endpoint: the endpoint to redirect to if the session key passes
                              Used to redirect away from login pages, if already logged in
        :param endpoint_kwargs: a dictionary of keyword arguments to pass to the redirect endpoint
        :param fail_json: JSON that is returned on failure - defaults to {"error": "You are not logged in."}
        :param fail_status: the status code to abort with if the session key does not exist or match the pass_value
        :param message: a message to add to flask.flash()
        :param message_category: the category of the flash message
        """
        self.token = token
        self.pass_endpoint = pass_endpoint
        self.fail_endpoint = fail_endpoint
        self.endpoint_kwargs = endpoint_kwargs
        self.fail_json = fail_json
        self.fail_status = fail_status
        self.message = message
        self.message_category = message_category


class SessionCheckpoint:
    session_key: str
    values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool]
    pass_endpoint: t.Optional[str] = None
    fail_endpoint: t.Optional[str] = None
    endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None
    fail_json: t.Optional[t.Dict[str, t.Any]] = None
    fail_status: int = 403
    message: t.Optional[str] = None
    message_category: str = "message"

    def __init__(
        self,
        session_key: str,
        values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
        pass_endpoint: t.Optional[str] = None,
        fail_endpoint: t.Optional[str] = None,
        endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
        fail_json: t.Optional[t.Dict[str, t.Any]] = None,
        fail_status: int = 403,
        message: t.Optional[str] = None,
        message_category: str = "message",
    ):
        """
        A checkpoint that checks if the specified session key exists and its value(s) match the specified value(s).

        If fail_json is provided, passing to endpoints will be disabled.

        :param session_key: the session key to check for
        :param values_allowed: a list of or singular value(s) that the session key must contain
        :param fail_endpoint: the endpoint to redirect to if the session key does not exist or
                              match the pass_value
        :param pass_endpoint: the endpoint to redirect to if the session key passes
                              Used to redirect away from login pages, if already logged in
        :param endpoint_kwargs: a dictionary of keyword arguments to pass to the redirect endpoint
        :param fail_json: JSON that is returned on failure - defaults to {"error": "You are not logged in."}
        :param fail_status: the status code to abort with if the session key does not exist or match the pass_value
        :param message: a message to add to flask.flash()
        :param message_category: the category of the flash message
        """
        self.session_key = session_key
        self.values_allowed = values_allowed
        self.pass_endpoint = pass_endpoint
        self.fail_endpoint = fail_endpoint
        self.endpoint_kwargs = endpoint_kwargs
        self.fail_json = fail_json
        self.fail_status = fail_status
        self.message = message
        self.message_category = message_category
