import logging
import os
import typing as t
from pathlib import Path

import toml as tml

from flask_imp import (
    FlaskConfig,
    ImpConfig as ImpConfigTemplate,
    DatabaseConfig,
    ImpBlueprintConfig as ImpConfigBlueprintTemplate,
)
from flask_imp.utilities import cast_to_int, cast_to_bool


def check_if_cast(
    cs_key, value, cast_key_value_to_str, cast_key_value_to_int, cast_key_value_to_bool
):
    if isinstance(cast_key_value_to_str, list):
        if cs_key in cast_key_value_to_str:
            return str(value)

    if isinstance(cast_key_value_to_int, list):
        if cs_key in cast_key_value_to_int:
            return cast_to_int(value)

    if isinstance(cast_key_value_to_bool, list):
        if cs_key in cast_key_value_to_bool:
            return bool(value)

    return value


def replace_env_value(value: t.Any) -> t.Any:
    """
    Replaces environment variables in the string with their values.
    """

    def attempt_to_find_env(v: str) -> t.Union[str, int, bool]:
        if v.lower() in os.environ:
            return os.getenv(v.lower())
        if v.upper() in os.environ:
            return os.getenv(v.upper())

        raise ValueError(f"Environment variable {v.lower()} or {v.upper()} not found.")

    if isinstance(value, str):
        if value.startswith("{{") and value.endswith("}}"):
            value = value[2:-2].strip()

            if ":" in value:
                val, type_ = value.split(":")
                value_found = attempt_to_find_env(val)

                if type_ == "int":
                    return cast_to_int(value_found)
                if type_ == "bool":
                    return cast_to_bool(value_found)

                return value_found

            return attempt_to_find_env(value)

    return value


def process_dict(
    this_dict: t.Optional[dict],
    key_case_switch: t.Literal["upper", "lower", "ignore"] = "upper",
    crawl: bool = False,
    rename_keys: t.Dict = None,
    cast_key_value_to_str: t.List[str] = None,
    cast_key_value_to_int: t.List[str] = None,
    cast_key_value_to_bool: t.List[str] = None,
) -> dict:
    """
    Used to process the config from_file dictionary. Turns all keys to upper case.

    rename_keys: {from: to}
    """

    if this_dict is None:
        return {}

    if rename_keys is None:
        rename_keys = {}

    return_dict = {}
    for key, value in this_dict.items():
        if key_case_switch == "ignore":
            cs_key = key
        else:
            cs_key = key.upper() if key_case_switch == "upper" else key.lower()

        if crawl:
            if isinstance(value, dict):
                return_dict[cs_key] = process_dict(
                    value,
                    key_case_switch,
                    crawl,
                    rename_keys,
                    cast_key_value_to_str,
                    cast_key_value_to_int,
                    cast_key_value_to_bool,
                )
                continue

        cs_key_final = cs_key if cs_key not in rename_keys else rename_keys[cs_key]
        final_value = replace_env_value(value)

        return_dict[cs_key_final] = check_if_cast(
            cs_key_final,
            final_value,
            cast_key_value_to_str,
            cast_key_value_to_int,
            cast_key_value_to_bool,
        )

    return return_dict


def load_app_toml(file: str, current_working_directory: Path) -> ImpConfigTemplate:
    """
    Processes the values from the configuration from_file.
    """
    config_file_path = current_working_directory / file

    if not config_file_path.exists():
        logging.critical("Config file was not found.")

    config = tml.loads(config_file_path.read_text())

    flask_config = process_dict(config.get("FLASK", {}))
    session_config = config.get("SESSION", {})
    sqlalchemy_config = config.get("SQLALCHEMY", {})

    database_config = process_dict(
        config.get("DATABASE"),
        key_case_switch="upper",
        crawl=True,
        rename_keys={"DATABASE_NAME": "NAME"},
        cast_key_value_to_int=["PORT"],
    )

    imp_config = ImpConfigTemplate()
    imp_config.FLASK = FlaskConfig(**flask_config, **sqlalchemy_config)

    imp_config.INIT_SESSION = session_config

    main_db = database_config.get("MAIN", {})
    if main_db:
        imp_config.DATABASE_MAIN = DatabaseConfig(**main_db)
        del database_config["MAIN"]

    imp_config.DATABASE_BINDS = {
        DatabaseConfig(
            **{**values, "BIND_KEY": db_key} if "BIND_KEY" not in values else values
        )
        for db_key, values in database_config.items()
    }

    return imp_config


def load_app_blueprint_toml(
    file: str, current_working_directory: Path
) -> ImpConfigBlueprintTemplate:
    """
    Processes the values from the configuration from_file.
    """
    config_file_path = current_working_directory / file

    if not config_file_path.exists():
        logging.critical("Config file was not found.")

    config = tml.loads(config_file_path.read_text())

    enabled_config = cast_to_bool(config.get("ENABLED", config.get("enabled", False)))
    settings_config = process_dict(config.get("SETTINGS", {}))
    session_config = config.get("INI_SESSION", config.get("SESSION", {}))

    database_config = process_dict(
        config.get("DATABASE_BINDS"),
        key_case_switch="upper",
        crawl=True,
        rename_keys={"DATABASE_NAME": "NAME"},
        cast_key_value_to_int=["PORT"],
    )

    imp_blueprint_config = ImpConfigBlueprintTemplate()
    imp_blueprint_config.set_using_args(
        enabled=enabled_config,
        **{k.lower(): v for k, v in settings_config.items()},
    )

    imp_blueprint_config.INIT_SESSION = session_config

    imp_blueprint_config.DATABASE_BINDS = {
        DatabaseConfig(
            **{**values, "BIND_KEY": db_key} if "BIND_KEY" not in values else values
        )
        for db_key, values in database_config.items()
    }

    return imp_blueprint_config
