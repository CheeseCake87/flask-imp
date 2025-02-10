import typing as t

from flask import Flask


class FlaskConfigObject:
    pass


class FlaskConfig:
    """
    Flask configuration class modeled after the Flask documentation.
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

    _additional: t.Dict[str, t.Any]

    _flask_config_keys = {
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
        debug: t.Optional[bool] = None,
        propagate_exceptions: t.Optional[bool] = None,
        trap_http_exceptions: t.Optional[bool] = None,
        trap_bad_request_errors: t.Optional[bool] = None,
        secret_key: t.Optional[str] = None,
        session_cookie_name: t.Optional[str] = None,
        session_cookie_domain: t.Optional[str] = None,
        session_cookie_path: t.Optional[str] = None,
        session_cookie_httponly: t.Optional[bool] = None,
        session_cookie_secure: t.Optional[bool] = None,
        session_cookie_samesite: t.Optional[t.Literal["Lax", "Strict"]] = None,
        permanent_session_lifetime: t.Optional[int] = None,
        session_refresh_each_request: t.Optional[bool] = None,
        use_x_sendfile: t.Optional[bool] = None,
        send_file_max_age_default: t.Optional[int] = None,
        error_404_help: t.Optional[bool] = None,
        server_name: t.Optional[str] = None,
        application_root: t.Optional[str] = None,
        preferred_url_scheme: t.Optional[str] = None,
        max_content_length: t.Optional[int] = None,
        templates_auto_reload: t.Optional[bool] = None,
        explain_template_loading: t.Optional[bool] = None,
        max_cookie_size: t.Optional[int] = None,
        app_instance: t.Optional[Flask] = None,
        additional: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> None:
        """
        Flask configuration class modeled after the Flask documentation.

        Additional config values can be set by passing them as a dict or using the set_additional method.

        All key arguments are converted to uppercase and added to the Flask app.config dictionary.
        e.g. session_cookie_name -> app.config["SESSION_COOKIE_NAME"]
        """
        self.DEBUG = debug
        self.PROPAGATE_EXCEPTIONS = propagate_exceptions
        self.TRAP_HTTP_EXCEPTIONS = trap_http_exceptions
        self.TRAP_BAD_REQUEST_ERRORS = trap_bad_request_errors
        self.SECRET_KEY = secret_key
        self.SESSION_COOKIE_NAME = session_cookie_name
        self.SESSION_COOKIE_DOMAIN = session_cookie_domain
        self.SESSION_COOKIE_PATH = session_cookie_path
        self.SESSION_COOKIE_HTTPONLY = session_cookie_httponly
        self.SESSION_COOKIE_SECURE = session_cookie_secure
        self.SESSION_COOKIE_SAMESITE = session_cookie_samesite
        self.PERMANENT_SESSION_LIFETIME = permanent_session_lifetime
        self.SESSION_REFRESH_EACH_REQUEST = session_refresh_each_request
        self.USE_X_SENDFILE = use_x_sendfile
        self.SEND_FILE_MAX_AGE_DEFAULT = send_file_max_age_default
        self.ERROR_404_HELP = error_404_help
        self.SERVER_NAME = server_name
        self.APPLICATION_ROOT = application_root
        self.PREFERRED_URL_SCHEME = preferred_url_scheme
        self.MAX_CONTENT_LENGTH = max_content_length
        self.TEMPLATES_AUTO_RELOAD = templates_auto_reload
        self.EXPLAIN_TEMPLATE_LOADING = explain_template_loading
        self.MAX_COOKIE_SIZE = max_cookie_size
        self._additional = additional or {}

        if app_instance is not None:
            self.init_app(app_instance)

    def set_additional(self, **kwargs: t.Any) -> None:
        """
        Set additional config values.
        Keys are converted to uppercase.
        """
        if kwargs:
            for k, v in kwargs.items():
                if k.upper() in self._flask_config_keys:
                    continue
                self._additional[k.upper()] = v

    def init_app(self, app: Flask) -> None:
        """
        Attach the configuration class to the Flask app instance.
        """
        if not isinstance(app, Flask):
            raise TypeError("The app that was passed in is not an instance of Flask")
        self.apply_config(app)

    def apply_config(self, app: Flask) -> None:
        """
        Apply the configuration to the Flask app instance.
        """
        if not isinstance(app, Flask):
            raise TypeError("The app that was passed in is not an instance of Flask")

        app.config.from_object(self.as_object())

    def as_dict(self) -> t.Dict[str, t.Any]:
        """
        Return the configuration as a dictionary.
        """
        dict_build = {}
        for attr in self._flask_config_keys:
            if hasattr(self, attr):
                this_attr = getattr(self, attr)

                if this_attr:  # if has value , add it
                    dict_build[attr] = this_attr

        for k, v in self._additional.items():
            if k.startswith("_"):
                continue

            if k.upper() not in self._flask_config_keys:
                dict_build[k.upper()] = v

        return dict_build

    def as_object(self) -> FlaskConfigObject:
        config_object = FlaskConfigObject()

        for k, v in self.as_dict().items():
            setattr(config_object, k, v)

        return config_object
