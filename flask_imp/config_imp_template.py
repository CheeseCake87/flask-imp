import typing as t
from dataclasses import dataclass

from flask_imp import FlaskConfig, DatabaseConfig


@dataclass
class ImpConfigTemplate:
    """
    FLASK: t.Union[dict, t.Type[FlaskConfigTemplate]]

    INIT_SESSION: t.Optional[dict]
    SQLITE_DB_EXTENSION: t.Optional[str]
    SQLITE_STORE_IN_PARENT: t.Optional[bool]

    DATABASE_MAIN: t.Optional[t.Union[dict, DatabaseConfig]]
    DATABASE_BINDS: t.Optional[
        t.Union[dict,t.List[DatabaseConfig]]
    ]
    """

    FLASK: t.Optional[FlaskConfig] = None

    INIT_SESSION: t.Optional[dict] = None

    SQLALCHEMY_ECHO: t.Optional[bool] = None
    SQLALCHEMY_TRACK_MODIFICATIONS: t.Optional[bool] = None
    SQLALCHEMY_RECORD_QUERIES: t.Optional[bool] = None

    SQLITE_DB_EXTENSION: t.Optional[str] = None
    SQLITE_STORE_IN_PARENT: t.Optional[bool] = None

    DATABASE_MAIN: t.Optional[DatabaseConfig] = None
    DATABASE_BINDS: t.Optional[t.Set[DatabaseConfig]] = None

    _attrs = (
        "FLASK",
        "INIT_SESSION",
        "DATABASE_MAIN",
        "DATABASE_BINDS",
    )

    _known_funcs = (
        "set_using_args",
        "set_app_config",
    )

    def __init__(self):
        pass

    def set_using_args(
        self,
        flask: FlaskConfig = None,
        init_session: t.Optional[dict] = None,
        sqlite_db_extension: t.Optional[str] = None,
        sqlite_store_in_parent: t.Optional[bool] = None,
        database_main: t.Optional[DatabaseConfig] = None,
        database_binds: t.Optional[t.Set[DatabaseConfig]] = None,
    ):
        if flask is not None:
            self.FLASK = flask
        if init_session is not None:
            self.INIT_SESSION = init_session
        if sqlite_db_extension is not None:
            self.SQLITE_DB_EXTENSION = sqlite_db_extension
        if sqlite_store_in_parent is not None:
            self.SQLITE_STORE_IN_PARENT = sqlite_store_in_parent
        if database_main is not None:
            self.DATABASE_MAIN = database_main
        if database_binds is not None:
            self.DATABASE_BINDS = database_binds
