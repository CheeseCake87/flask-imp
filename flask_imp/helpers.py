import logging
import os
import typing as t
from pathlib import Path

from flask import Flask
from toml import load as toml_load

from ._cli.filelib import AppFileLib

from .utilities import cast_to_bool, process_dict


def _build_database_uri(
    database_config_value: dict, app_instance: Flask
) -> t.Optional[str]:
    """
    Puts together the correct database URI depending on the type specified.

    Fails if type is not supported.
    """

    app_root = Path(app_instance.root_path)
    db_dialect = database_config_value.get("DIALECT", "None")
    db_name = database_config_value.get("DATABASE_NAME", "database")
    db_location = database_config_value.get("LOCATION", "instance")
    db_port = str(database_config_value.get("PORT", "None"))
    db_username = database_config_value.get("USERNAME", "None")
    db_password = database_config_value.get("PASSWORD", "None")

    allowed_dialects = ("postgresql", "mysql", "oracle", "sqlite", "mssql")

    if db_dialect == "None":
        raise ValueError(
            """\
Database dialect was not specified, must be: postgresql / mysql / oracle / sqlite / mssql
Example:

[DATABASE.MAIN]
ENABLED = true
DIALECT = "sqlite"
DATABASE_NAME = "database"
LOCATION = "instance"
PORT = ""
USERNAME = "database"
PASSWORD = "password"

This will create a sqlite file called
database.sqlite in a folder called instance.

You can change the file extension by setting the environment variable IMP_SQLITE_DB_EXTENSION"""
        )

    if not db_location:
        db_location = "instance"

    if "sqlite" in db_dialect:
        set_db_extension = app_instance.config.get("SQLITE_DB_EXTENSION", ".sqlite")
        store_db_in_parent = cast_to_bool(
            app_instance.config.get("SQLITE_STORE_IN_PARENT", False)
        )

        if store_db_in_parent:
            db_location_path = Path(app_root.parent / db_location)
        else:
            db_location_path = Path(app_root / db_location)

        db_location_path.mkdir(parents=True, exist_ok=True)
        db_location_file_path = db_location_path / f"{db_name}{set_db_extension}"
        return f"{db_dialect}:///{db_location_file_path}"

    for dialect in allowed_dialects:
        if dialect in db_dialect:
            return f"{db_dialect}://{db_username}:{db_password}@{db_location}:{db_port}/{db_name}"

    raise ValueError(
        """\
Database dialect is unknown, must be: postgresql / mysql / oracle / sqlite / mssql

Example:

[DATABASE.MAIN]
ENABLED = true
DIALECT = "sqlite"
DATABASE_NAME = "database"
LOCATION = "instance"
PORT = ""
USERNAME = "database"
PASSWORD = "password"

This will create a sqlite file called
database.sqlite in a folder called instance.

You can change the file extension by setting the environment variable IMP_SQLITE_DB_EXTENSION"""
    )


def _init_app_config(
    config_file_path: Path, ignore_missing_env_variables: bool, app
) -> dict:
    """
    Processes the values from the configuration from_file.
    """
    if not config_file_path.exists():
        logging.critical(
            "Config file was not found, creating default.config.toml to use"
        )

        config_file_path.write_text(
            AppFileLib.default_config_toml.format(secret_key=os.urandom(24).hex())
        )

    config_suffix = (".toml", ".tml")

    if config_file_path.suffix not in config_suffix:
        raise TypeError(
            "Config from_file must be one of the following types: .toml / .tml"
        )

    config = process_dict(toml_load(config_file_path))

    flask_config = process_dict(
        config.get("FLASK"),
        key_case_switch="upper",
        ignore_missing_env_variables=ignore_missing_env_variables,
    )
    session_config = process_dict(
        config.get("SESSION"),
        key_case_switch="ignore",
        ignore_missing_env_variables=ignore_missing_env_variables,
    )
    sqlalchemy_config = process_dict(
        config.get("SQLALCHEMY"),
        key_case_switch="upper",
        ignore_missing_env_variables=ignore_missing_env_variables,
    )
    database_config = process_dict(
        config.get("DATABASE"),
        key_case_switch="upper",
        ignore_missing_env_variables=ignore_missing_env_variables,
        crawl=True,
    )

    if flask_config is not None and isinstance(flask_config, dict):
        for flask_config_key, flask_config_value in flask_config.items():
            app.config.update({flask_config_key: flask_config_value})

    if sqlalchemy_config is not None and isinstance(sqlalchemy_config, dict):
        for sqlalchemy_config_key, sqlalchemy_config_value in sqlalchemy_config.items():
            app.config.update({sqlalchemy_config_key: sqlalchemy_config_value})

    if database_config is not None and isinstance(database_config, dict):
        app.config["SQLALCHEMY_BINDS"] = dict()
        for database_config_key, database_config_values in database_config.items():
            if database_config_values.get("ENABLED", False):
                database_uri = _build_database_uri(database_config_values, app)
                if database_uri:
                    if database_config_key == "MAIN":
                        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
                        continue

                    app.config["SQLALCHEMY_BINDS"].update(
                        {str(database_config_key).lower(): database_uri}
                    )

    return {
        "FLASK": {**flask_config, **sqlalchemy_config},
        "SESSION": session_config,
        "DATABASE": database_config,
    }


def _init_bp_config(blueprint_name: str, config_file_path: Path) -> tuple:
    """
    Attempts to load and process the blueprint configuration file.
    """

    if not config_file_path.exists():
        raise FileNotFoundError(
            f"{blueprint_name} Blueprint config {config_file_path.name} was not found"
        )

    config_suffix = (".toml", ".tml")

    if config_file_path.suffix not in config_suffix:
        raise TypeError(
            "Blueprint Config must be one of the following types: .toml / .tml"
        )

    config = process_dict(toml_load(config_file_path), key_case_switch="upper")
    enabled = cast_to_bool(config.get("ENABLED", False))

    if not enabled:
        return enabled, {}, {}, {}

    session = process_dict(config.get("SESSION", {}), key_case_switch="ignore")
    settings = process_dict(config.get("SETTINGS", {}), key_case_switch="lower")
    database_bind = process_dict(
        config.get("DATABASE_BIND", {}), key_case_switch="upper"
    )

    kwargs = {}

    valid_settings = (
        "url_prefix",
        "subdomain",
        "url_defaults",
        "static_folder",
        "template_folder",
        "static_url_path",
        "root_path",
    )

    for setting in valid_settings:
        if setting == "url_prefix":
            kwargs.update(
                {
                    "url_prefix": settings.get("url_prefix")
                    if settings.get("url_prefix") != ""
                    else f"/{blueprint_name}"
                }
            )
            continue
        if setting in settings:
            if settings.get(setting, False):
                kwargs.update({setting: settings.get(setting)})

    return enabled, session, settings, database_bind
