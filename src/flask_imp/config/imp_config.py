import typing as t
from dataclasses import dataclass

from flask import Flask
from flask_imp.config import DatabaseConfig


@dataclass
class ImpConfig:
    IMP_INIT_SESSION: t.Optional[t.Dict[str, t.Any]]

    IMP_DATABASE_MAIN: t.Optional[DatabaseConfig]
    IMP_DATABASE_BINDS: t.Optional[t.List[DatabaseConfig]]

    def __init__(
        self,
        init_session: t.Optional[t.Dict[str, t.Any]] = None,
        database_main: t.Optional[DatabaseConfig] = None,
        database_binds: t.Optional[t.List[DatabaseConfig]] = None,
    ):
        if not init_session:
            self.IMP_INIT_SESSION = {}
        else:
            self.IMP_INIT_SESSION = init_session

        self.IMP_DATABASE_MAIN = database_main

        if database_binds is None:
            self.IMP_DATABASE_BINDS = []
        else:
            self.IMP_DATABASE_BINDS = database_binds

    def load_config_from_flask(self, app: Flask) -> None:
        _init_session = app.config.get("IMP_INIT_SESSION")
        _database_main = app.config.get("IMP_DATABASE_MAIN")
        _database_binds = app.config.get("IMP_DATABASE_BINDS")

        if not isinstance(_init_session, dict):
            if _init_session is not None:
                raise ValueError("IMP_INIT_SESSION must be a dict")
        else:
            self.IMP_INIT_SESSION = app.config["IMP_INIT_SESSION"]

        if isinstance(_database_main, dict):
            for key in _database_main:
                if key == "dialect":
                    if _database_main[key] not in DatabaseConfig.allowed_dialects:
                        raise ValueError(
                            f"Database dialect must be one of: {', '.join(DatabaseConfig.allowed_dialects)}"
                        )

                if not hasattr(DatabaseConfig, key):
                    raise ValueError(f"DatabaseConfig has no attribute: {key}")

            self.IMP_DATABASE_MAIN = DatabaseConfig(**app.config["IMP_DATABASE_MAIN"])

        if "IMP_DATABASE_BINDS" in app.config:
            if not isinstance(_database_binds, list):
                if _database_binds is not None:
                    raise ValueError("IMP_DATABASE_BINDS must be of type list")

            else:
                for db in app.config["IMP_DATABASE_BINDS"]:
                    for key in db:
                        if key == "dialect":
                            if db[key] not in DatabaseConfig.allowed_dialects:
                                raise ValueError(
                                    f"Database dialect must be one of: {', '.join(DatabaseConfig.allowed_dialects)}"
                                )

                        if not hasattr(DatabaseConfig, key):
                            raise ValueError(f"DatabaseConfig has no attribute: {key}")

            self.IMP_DATABASE_BINDS = [
                DatabaseConfig(**db) for db in app.config["IMP_DATABASE_BINDS"]
            ]
