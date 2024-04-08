import typing as t


class FlaskConfigTemplate:
    """
    DEBUG: t.Optional[bool]
    PROPAGATE_EXCEPTIONS: t.Optional[bool]
    TRAP_HTTP_EXCEPTIONS: t.Optional[bool]
    TRAP_BAD_REQUEST_ERRORS: t.Optional[bool]
    SECRET_KEY: t.Optional[str]
    SESSION_COOKIE_NAME: t.Optional[str]
    SESSION_COOKIE_DOMAIN: t.Optional[str]
    SESSION_COOKIE_PATH: t.Optional[str]
    SESSION_COOKIE_HTTPONLY: t.Optional[bool]
    SESSION_COOKIE_SECURE: t.Optional[bool]
    SESSION_COOKIE_SAMESITE: t.Optional[t.Literal["Lax", "Strict"]]
    PERMANENT_SESSION_LIFETIME: t.Optional[int]
    SESSION_REFRESH_EACH_REQUEST: t.Optional[bool]
    USE_X_SENDFILE: t.Optional[bool]
    SEND_FILE_MAX_AGE_DEFAULT: t.Optional[int]
    ERROR_404_HELP: t.Optional[bool]
    SERVER_NAME: t.Optional[str]
    APPLICATION_ROOT: t.Optional[str]
    PREFERRED_URL_SCHEME: t.Optional[str]
    MAX_CONTENT_LENGTH: t.Optional[int]
    TEMPLATES_AUTO_RELOAD: t.Optional[bool]
    EXPLAIN_TEMPLATE_LOADING: t.Optional[bool]
    MAX_COOKIE_SIZE: t.Optional[int]
    """

    DEBUG: t.Optional[bool]
    PROPAGATE_EXCEPTIONS: t.Optional[bool]
    TRAP_HTTP_EXCEPTIONS: t.Optional[bool]
    TRAP_BAD_REQUEST_ERRORS: t.Optional[bool]
    SECRET_KEY: t.Optional[str]
    SESSION_COOKIE_NAME: t.Optional[str]
    SESSION_COOKIE_DOMAIN: t.Optional[str]
    SESSION_COOKIE_PATH: t.Optional[str]
    SESSION_COOKIE_HTTPONLY: t.Optional[bool]
    SESSION_COOKIE_SECURE: t.Optional[bool]
    SESSION_COOKIE_SAMESITE: t.Optional[t.Literal["Lax", "Strict"]]
    PERMANENT_SESSION_LIFETIME: t.Optional[int]
    SESSION_REFRESH_EACH_REQUEST: t.Optional[bool]
    USE_X_SENDFILE: t.Optional[bool]
    SEND_FILE_MAX_AGE_DEFAULT: t.Optional[int]
    ERROR_404_HELP: t.Optional[bool]
    SERVER_NAME: t.Optional[str]
    APPLICATION_ROOT: t.Optional[str]
    PREFERRED_URL_SCHEME: t.Optional[str]
    MAX_CONTENT_LENGTH: t.Optional[int]
    TEMPLATES_AUTO_RELOAD: t.Optional[bool]
    EXPLAIN_TEMPLATE_LOADING: t.Optional[bool]
    MAX_COOKIE_SIZE: t.Optional[int]

    _attrs = {
        "DEBUG",
        "PROPAGATE_EXCEPTIONS",
        "TRAP_HTTP_EXCEPTIONS",
        "TRAP_BAD_REQUEST_ERRORS",
        "SECRET_KEY",
        "SESSION_COOKIE_NAME",
        "SESSION_COOKIE_DOMAIN",
        "SESSION_COOKIE_PATH",
        "SESSION_COOKIE_HTTPONLY",
        "SESSION_COOKIE_SECURE",
        "SESSION_COOKIE_SAMESITE",
        "PERMANENT_SESSION_LIFETIME",
        "SESSION_REFRESH_EACH_REQUEST",
        "USE_X_SENDFILE",
        "SEND_FILE_MAX_AGE_DEFAULT",
        "ERROR_404_HELP",
        "SERVER_NAME",
        "APPLICATION_ROOT",
        "PREFERRED_URL_SCHEME",
        "MAX_CONTENT_LENGTH",
        "TEMPLATES_AUTO_RELOAD",
        "EXPLAIN_TEMPLATE_LOADING",
        "MAX_COOKIE_SIZE",
    }

    def __init__(
        self,
        DEBUG: t.Optional[bool] = None,  # noqa
        PROPAGATE_EXCEPTIONS: t.Optional[bool] = None,  # noqa
        TRAP_HTTP_EXCEPTIONS: t.Optional[bool] = None,  # noqa
        TRAP_BAD_REQUEST_ERRORS: t.Optional[bool] = None,  # noqa
        SECRET_KEY: t.Optional[str] = None,  # noqa
        SESSION_COOKIE_NAME: t.Optional[str] = None,  # noqa
        SESSION_COOKIE_DOMAIN: t.Optional[str] = None,  # noqa
        SESSION_COOKIE_PATH: t.Optional[str] = None,  # noqa
        SESSION_COOKIE_HTTPONLY: t.Optional[bool] = None,  # noqa
        SESSION_COOKIE_SECURE: t.Optional[bool] = None,  # noqa
        SESSION_COOKIE_SAMESITE: t.Optional[t.Literal["Lax", "Strict"]] = None,  # noqa
        PERMANENT_SESSION_LIFETIME: t.Optional[int] = None,  # noqa
        SESSION_REFRESH_EACH_REQUEST: t.Optional[bool] = None,  # noqa
        USE_X_SENDFILE: t.Optional[bool] = None,  # noqa
        SEND_FILE_MAX_AGE_DEFAULT: t.Optional[int] = None,  # noqa
        ERROR_404_HELP: t.Optional[bool] = None,  # noqa
        SERVER_NAME: t.Optional[str] = None,  # noqa
        APPLICATION_ROOT: t.Optional[str] = None,  # noqa
        PREFERRED_URL_SCHEME: t.Optional[str] = None,  # noqa
        MAX_CONTENT_LENGTH: t.Optional[int] = None,  # noqa
        TEMPLATES_AUTO_RELOAD: t.Optional[bool] = None,  # noqa
        EXPLAIN_TEMPLATE_LOADING: t.Optional[bool] = None,  # noqa
        MAX_COOKIE_SIZE: t.Optional[int] = None,  # noqa
        **kwargs,
    ):
        self.set_using_args(
            **{
                attr.upper(): val
                for attr, val in locals().items()
                if attr in self._attrs
            }
        )
        self.set_from_dict(kwargs)

    def set_using_args(
        self,
        DEBUG: t.Optional[bool] = None,  # noqa
        PROPAGATE_EXCEPTIONS: t.Optional[bool] = None,  # noqa
        TRAP_HTTP_EXCEPTIONS: t.Optional[bool] = None,  # noqa
        TRAP_BAD_REQUEST_ERRORS: t.Optional[bool] = None,  # noqa
        SECRET_KEY: t.Optional[str] = None,  # noqa
        SESSION_COOKIE_NAME: t.Optional[str] = None,  # noqa
        SESSION_COOKIE_DOMAIN: t.Optional[str] = None,  # noqa
        SESSION_COOKIE_PATH: t.Optional[str] = None,  # noqa
        SESSION_COOKIE_HTTPONLY: t.Optional[bool] = None,  # noqa
        SESSION_COOKIE_SECURE: t.Optional[bool] = None,  # noqa
        SESSION_COOKIE_SAMESITE: t.Optional[t.Literal["Lax", "Strict"]] = None,  # noqa
        PERMANENT_SESSION_LIFETIME: t.Optional[int] = None,  # noqa
        SESSION_REFRESH_EACH_REQUEST: t.Optional[bool] = None,  # noqa
        USE_X_SENDFILE: t.Optional[bool] = None,  # noqa
        SEND_FILE_MAX_AGE_DEFAULT: t.Optional[int] = None,  # noqa
        ERROR_404_HELP: t.Optional[bool] = None,  # noqa
        SERVER_NAME: t.Optional[str] = None,  # noqa
        APPLICATION_ROOT: t.Optional[str] = None,  # noqa
        PREFERRED_URL_SCHEME: t.Optional[str] = None,  # noqa
        MAX_CONTENT_LENGTH: t.Optional[int] = None,  # noqa
        TEMPLATES_AUTO_RELOAD: t.Optional[bool] = None,  # noqa
        EXPLAIN_TEMPLATE_LOADING: t.Optional[bool] = None,  # noqa
        MAX_COOKIE_SIZE: t.Optional[int] = None,  # noqa
    ):
        if DEBUG is not None:
            self.DEBUG = DEBUG
        if PROPAGATE_EXCEPTIONS is not None:
            self.PROPAGATE_EXCEPTIONS = PROPAGATE_EXCEPTIONS
        if TRAP_HTTP_EXCEPTIONS is not None:
            self.TRAP_HTTP_EXCEPTIONS = TRAP_HTTP_EXCEPTIONS
        if TRAP_BAD_REQUEST_ERRORS is not None:
            self.TRAP_BAD_REQUEST_ERRORS = TRAP_BAD_REQUEST_ERRORS
        if SECRET_KEY is not None:
            self.SECRET_KEY = SECRET_KEY
        if SESSION_COOKIE_NAME is not None:
            self.SESSION_COOKIE_NAME = SESSION_COOKIE_NAME
        if SESSION_COOKIE_DOMAIN is not None:
            self.SESSION_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN
        if SESSION_COOKIE_PATH is not None:
            self.SESSION_COOKIE_PATH = SESSION_COOKIE_PATH
        if SESSION_COOKIE_HTTPONLY is not None:
            self.SESSION_COOKIE_HTTPONLY = SESSION_COOKIE_HTTPONLY
        if SESSION_COOKIE_SECURE is not None:
            self.SESSION_COOKIE_SECURE = SESSION_COOKIE_SECURE
        if SESSION_COOKIE_SAMESITE is not None:
            self.SESSION_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE
        if PERMANENT_SESSION_LIFETIME is not None:
            self.PERMANENT_SESSION_LIFETIME = PERMANENT_SESSION_LIFETIME
        if SESSION_REFRESH_EACH_REQUEST is not None:
            self.SESSION_REFRESH_EACH_REQUEST = SESSION_REFRESH_EACH_REQUEST
        if USE_X_SENDFILE is not None:
            self.USE_X_SENDFILE = USE_X_SENDFILE
        if SEND_FILE_MAX_AGE_DEFAULT is not None:
            self.SEND_FILE_MAX_AGE_DEFAULT = SEND_FILE_MAX_AGE_DEFAULT
        if ERROR_404_HELP is not None:
            self.ERROR_404_HELP = ERROR_404_HELP
        if SERVER_NAME is not None:
            self.SERVER_NAME = SERVER_NAME
        if APPLICATION_ROOT is not None:
            self.APPLICATION_ROOT = APPLICATION_ROOT
        if PREFERRED_URL_SCHEME is not None:
            self.PREFERRED_URL_SCHEME = PREFERRED_URL_SCHEME
        if MAX_CONTENT_LENGTH is not None:
            self.MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
        if TEMPLATES_AUTO_RELOAD is not None:
            self.TEMPLATES_AUTO_RELOAD = TEMPLATES_AUTO_RELOAD
        if EXPLAIN_TEMPLATE_LOADING is not None:
            self.EXPLAIN_TEMPLATE_LOADING = EXPLAIN_TEMPLATE_LOADING
        if MAX_COOKIE_SIZE is not None:
            self.MAX_COOKIE_SIZE = MAX_COOKIE_SIZE

    def set(self, key, value):
        setattr(self, key.upper(), value)

    def set_from_dict(self, config_dict: dict):
        for key, value in config_dict.items():
            self._attrs.add(key.upper())
            setattr(self, key.upper(), value)

    def attrs(self) -> t.Set[t.Tuple[str, t.Union[bool, str, int]]]:
        return {
            (attr, getattr(self, attr))
            for attr in self._attrs
            if hasattr(self, attr) and getattr(self, attr) is not None
        }


if __name__ == "__main__":
    f = FlaskConfigTemplate()
