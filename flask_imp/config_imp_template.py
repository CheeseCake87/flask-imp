import typing as t
from dataclasses import dataclass
from pathlib import Path

from flask_imp import FlaskConfigTemplate, DatabaseConfigTemplate
from flask_imp.protocols import Flask
from flask_imp.utilities import build_database_main, build_database_binds


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

    FLASK: t.Optional[FlaskConfigTemplate] = None

    INIT_SESSION: t.Optional[dict] = None

    SQLALCHEMY_ECHO: t.Optional[bool] = None
    SQLALCHEMY_TRACK_MODIFICATIONS: t.Optional[bool] = None
    SQLALCHEMY_RECORD_QUERIES: t.Optional[bool] = None

    SQLITE_DB_EXTENSION: t.Optional[str] = None
    SQLITE_STORE_IN_PARENT: t.Optional[bool] = None

    DATABASE_MAIN: t.Optional[DatabaseConfigTemplate] = None
    DATABASE_BINDS: t.Optional[t.Set[DatabaseConfigTemplate]] = None

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
        for attr in self._attrs:
            setattr(self, attr, None)

    def set_using_args(
            self,
            flask: FlaskConfigTemplate = None,
            init_session: t.Optional[dict] = None,
            sqlite_db_extension: t.Optional[str] = None,
            sqlite_store_in_parent: t.Optional[bool] = None,
            database_main: t.Optional[DatabaseConfigTemplate] = None,
            database_binds: t.Optional[t.Set[DatabaseConfigTemplate]] = None,
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

    def set_app_config(self, flask_app: Flask, app_path: Path):
        # Set Flask config
        flask_app.config.update(**{attr[0]: attr[1] for attr in self.FLASK.attrs()})

        # Set additional config, skip if already set in Flask config
        _allowed_types = (str, bool, int, float, dict, list, set)

        for attr in self.__dir__():
            if attr not in self._attrs and attr not in self._known_funcs:
                _ = getattr(self, attr)
                if (
                        not attr.startswith("_")
                        and _ is not None
                        and type(attr) in _allowed_types
                        and attr not in flask_app.config
                ):
                    flask_app.config[attr] = getattr(self, attr)

        build_database_main(flask_app, app_path, self.DATABASE_MAIN)
        build_database_binds(flask_app, app_path, self.DATABASE_BINDS)
