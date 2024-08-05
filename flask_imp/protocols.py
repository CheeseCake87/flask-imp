import typing as t
from pathlib import Path

ImpBlueprintSelf = t.TypeVar("ImpBlueprintSelf", bound="ImpBlueprint")


@t.runtime_checkable
class Blueprint(t.Protocol):
    root_path: str


@t.runtime_checkable
class ImpBlueprint(t.Protocol):
    bp_name: str
    enabled: bool
    config: t.Any
    package: str
    location: Path

    _models: t.Set
    _nested_blueprints: t.Union[t.Set, t.Set[t.Any]]

    def register_blueprint(self, blueprint: Blueprint): ...

    def _register(self, app: "Flask", options: dict) -> None: ...

    def load_config(self, imp_instance) -> None: ...

    def super_settings(self) -> dict: ...


@t.runtime_checkable
class Flask(t.Protocol):
    name: str
    root_path: str
    extensions: dict
    config: dict
    static_folder: t.Optional[str]
    template_folder: t.Optional[str]

    logger: t.Any

    app_context: t.Any

    def register_blueprint(self, blueprint: t.Union[Blueprint, ImpBlueprint]): ...

    @property
    def before_request(self): ...


@t.runtime_checkable
class Imp(t.Protocol):
    app: Flask
    config: t.Any
    app_path: Path

    def import_models(self, path: str) -> None: ...


@t.runtime_checkable
class FlaskConfig(t.Protocol):
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

    def set_using_args(
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
    ): ...

    def _get_attr_values(self) -> t.Set[t.Tuple[str, t.Union[bool, str, int]]]: ...

    def attrs(self) -> t.Set[t.Tuple[str, t.Union[bool, str, int]]]: ...


@t.runtime_checkable
class DatabaseConfig(t.Protocol):
    enabled: bool
    dialect: t.Literal["mysql", "postgresql", "sqlite", "oracle", "mssql"]
    name: str
    bind_key: str
    location: str
    port: int
    username: str
    password: str

    def __init__(self): ...

    def as_dict(self) -> dict: ...


@t.runtime_checkable
class ImpConfig(t.Protocol):
    FLASK: FlaskConfig

    INIT_SESSION: t.Optional[dict]

    SQLALCHEMY_ECHO: t.Optional[bool]
    SQLALCHEMY_TRACK_MODIFICATIONS: t.Optional[bool]
    SQLALCHEMY_RECORD_QUERIES: t.Optional[bool]

    SQLITE_DB_EXTENSION: t.Optional[str]
    SQLITE_STORE_IN_PARENT: t.Optional[bool]

    DATABASE_MAIN: t.Optional[DatabaseConfig]
    DATABASE_BINDS: t.Optional[t.Set[DatabaseConfig]]

    def __call__(self, *args, **kwargs): ...


@t.runtime_checkable
class ImpBlueprintConfig(t.Protocol):
    ENABLED: bool
    URL_PREFIX: str
    SUBDOMAIN: str
    URL_DEFAULTS: dict
    STATIC_FOLDER: str
    TEMPLATE_FOLDER: str
    STATIC_URL_PATH: str
    ROOT_PATH: str
    CLI_GROUP: str

    INIT_SESSION: dict

    DATABASE_BINDS: t.Optional[t.Set[DatabaseConfig]]

    def __call__(self, *args, **kwargs): ...
