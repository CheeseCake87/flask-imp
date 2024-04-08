import logging
import tomllib
import typing as t
from pathlib import Path
from pprint import pprint

from flask_imp import FlaskConfigTemplate, ImpConfigTemplate, DatabaseConfigTemplate
from flask_imp.utilities import cast_to_int


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

        return_dict[cs_key_final] = check_if_cast(
            cs_key_final,
            value,
            cast_key_value_to_str,
            cast_key_value_to_int,
            cast_key_value_to_bool,
        )

    return return_dict


def load_toml(file: str, current_working_directory: Path) -> ImpConfigTemplate:
    """
    Processes the values from the configuration from_file.
    """
    config_file_path = current_working_directory / file

    if not config_file_path.exists():
        logging.critical(
            "Config file was not found, creating default.config.toml to use"
        )

    config = tomllib.loads(config_file_path.read_text())

    flask_config = process_dict(config.get("FLASK", {}))
    session_config = config.get("SESSION", {})
    sqlalchemy_config = config.get("SQLALCHEMY", {})

    database_config = process_dict(
        config.get("DATABASE"),
        key_case_switch="lower",
        crawl=True,
        rename_keys={"database_name": "name"},
        cast_key_value_to_int=["port"],
    )

    pprint(sqlalchemy_config)

    imp_config = ImpConfigTemplate()
    imp_config.FLASK = FlaskConfigTemplate(**flask_config, **sqlalchemy_config)

    imp_config.INIT_SESSION = session_config

    main_db = database_config.get("main", {})
    if main_db:
        imp_config.DATABASE_MAIN = DatabaseConfigTemplate(**main_db)
        del database_config["main"]

    imp_config.DATABASE_BINDS = {
        DatabaseConfigTemplate(
            **{**values, "bind_key": db_key} if "bind_key" not in values else values
        )
        for db_key, values in database_config.items()
    }

    return imp_config


if __name__ == "__main__":
    load_toml("default.config.toml", Path("/Users/david/PycharmProjects/flask-imp/app"))
