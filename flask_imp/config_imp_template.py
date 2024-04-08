import typing as t
from pathlib import Path

from flask_imp import FlaskConfigTemplate, DatabaseConfigTemplate
from flask_imp.protocols import Flask


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

    FLASK: t.Optional[FlaskConfigTemplate]

    INIT_SESSION: t.Optional[dict]

    SQLALCHEMY_ECHO: t.Optional[bool]
    SQLALCHEMY_TRACK_MODIFICATIONS: t.Optional[bool]
    SQLALCHEMY_RECORD_QUERIES: t.Optional[bool]

    SQLITE_DB_EXTENSION: t.Optional[str]
    SQLITE_STORE_IN_PARENT: t.Optional[bool]

    DATABASE_MAIN: t.Optional[DatabaseConfigTemplate]
    DATABASE_BINDS: t.Optional[t.Set[DatabaseConfigTemplate]]

    _attrs = (
        "FLASK",
        "INIT_SESSION",
        "DATABASE_MAIN",
        "DATABASE_BINDS",
    )

    _addi_attrs = (
        "SQLALCHEMY_ECHO",
        "SQLALCHEMY_TRACK_MODIFICATIONS",
        "SQLALCHEMY_RECORD_QUERIES",
        "SQLITE_DB_EXTENSION",
        "SQLITE_STORE_IN_PARENT",
    )

    def __init__(self):
        pass

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
        for attr in self._addi_attrs:
            if (
                    hasattr(self, attr)
                    and getattr(self, attr) is not None
                    and attr not in flask_app.config
            ):
                flask_app.config[attr] = getattr(self, attr)

        # Set database URI
        if self.DATABASE_MAIN:
            if self.DATABASE_MAIN.enabled:
                flask_app.config["SQLALCHEMY_DATABASE_URI"] = self._build_database_uri(
                    flask_app, app_path, self.DATABASE_MAIN
                )

        if self.DATABASE_BINDS:
            for db in self.DATABASE_BINDS:
                if db.enabled:
                    if "SQLALCHEMY_BINDS" not in flask_app.config:
                        flask_app.config["SQLALCHEMY_BINDS"] = {}

                    flask_app.config["SQLALCHEMY_BINDS"][db.bind_key] = self._build_database_uri(
                        flask_app, app_path, db
                    )

    def _build_database_uri(
            self, flask_app: Flask, app_path: Path, db: DatabaseConfigTemplate
    ):
        if db.dialect == "sqlite":
            filepath = (
                    app_path
                    / "instance"
                    / (
                        db.name + self.SQLITE_DB_EXTENSION
                        if self.SQLITE_DB_EXTENSION
                        else flask_app.config.get("SQLITE_DB_EXTENSION", ".sqlite")
                    )
            )
            return f"{db.dialect}:///{filepath}"

        return (
            f"{db.dialect}://{db.username}:"
            f"{db.password}@{db.location}:"
            f"{db.port}/{db.name}"
        )
