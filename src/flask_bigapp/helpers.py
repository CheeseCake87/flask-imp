import logging
import os
from pathlib import Path

from toml import load as toml_load

from .resources import Resources
from .utilities import if_env_replace, capitalize_dict_keys, cast_to_bool, lower_dict_keys


def build_database_uri(database_config_value: dict, app) -> str:
    """
    Puts together the correct database URI depending on the type specified.

    Fails if type is not supported.
    """
    app_root = Path(app.root_path)

    db_type = if_env_replace(database_config_value.get("TYPE", "None"))
    db_name = if_env_replace(database_config_value.get('DATABASE_NAME', 'database'))

    db_location = if_env_replace(database_config_value.get("LOCATION", "db"))
    db_port = if_env_replace(str(database_config_value.get('PORT', 'None')))

    db_username = if_env_replace(database_config_value.get('USERNAME', 'None'))
    db_password = if_env_replace(database_config_value.get('PASSWORD', 'None'))

    db_allowed = ('postgresql', 'mysql', 'oracle')

    if db_type == "sqlite":
        if db_location is not None:

            if Path(db_location).exists():
                database = Path(db_location / f"{db_name}.db")
                return f"sqlite:///{database}"

            db_location_path = Path(app_root / db_location)
            db_location_path.mkdir(parents=True, exist_ok=True)
            db_location_file_path = db_location_path / f"{db_name}.db"
            return f"sqlite:///{db_location_file_path}"

        db_at_root = Path(app_root / f"{db_name}.db")
        return f"{db_type}:///{db_at_root}"

    if db_type in db_allowed:
        return f"{db_type}://{db_username}:{db_password}@{db_location}:{db_port}/{db_name}"

    raise ValueError(
        "Unknown database type, must be: postgresql / mysql / oracle / sqlite")


def init_app_config(config_file_path: Path, app) -> dict:
    """
    Processes the values from the configuration from_file.
    """
    if not config_file_path.exists():
        logging.critical("Config file was not found, creating default.config.toml to use")

        config_file_path.write_text(
            Resources.default_config.format(
                secret_key=os.urandom(24).hex())
        )

    config_suffix = ('.toml', '.tml')

    if config_file_path.suffix not in config_suffix:
        raise TypeError("Config from_file must be one of the following types: .toml / .tml")

    config = capitalize_dict_keys(toml_load(config_file_path))
    flask_config = capitalize_dict_keys(config.get("FLASK"))
    session_config = config.get("SESSION")
    database_config = capitalize_dict_keys(config.get("DATABASE"))

    if flask_config is not None and isinstance(flask_config, dict):
        for flask_config_key, flask_config_value in flask_config.items():
            app.config.update({str(flask_config_key): if_env_replace(flask_config_value)})

    if database_config is not None and isinstance(database_config, dict):
        app.config['SQLALCHEMY_BINDS'] = dict()
        for database_config_key, database_config_values in database_config.items():
            values = capitalize_dict_keys(database_config_values)
            if values.get("ENABLED", False):
                if database_config_key == "MAIN":
                    app.config['SQLALCHEMY_DATABASE_URI'] = f"{build_database_uri(values, app)}"
                    continue

                app.config['SQLALCHEMY_BINDS'].update({
                    str(database_config_key).lower(): f"{build_database_uri(values, app)}"
                })

    return {"FLASK": flask_config, "SESSION": session_config, "DATABASE": database_config}


def init_bp_config(blueprint_name: str, config_file_path: Path) -> tuple:
    """
    Attempts to load the and process the configuration from_file.
    """

    if not config_file_path.exists():
        raise FileNotFoundError(f"{blueprint_name} Blueprint config from_file {config_file_path.name} was not found")

    config_suffix = ('.toml', '.tml')

    if config_file_path.suffix not in config_suffix:
        raise TypeError("Config from_file must be one of the following types: .toml / .tml")

    config = capitalize_dict_keys(toml_load(config_file_path))

    enabled = cast_to_bool(config.get('ENABLED', False))

    if not enabled:
        return enabled, {}, {}

    session = config.get('SESSION', {})
    settings = lower_dict_keys(config.get('SETTINGS', {}))

    kwargs = dict()

    valid_settings = (
        'url_prefix', 'subdomain', 'url_defaults', 'static_folder', 'template_folder', 'static_url_path', 'root_path'
    )

    for setting in valid_settings:
        if setting == 'url_prefix':
            kwargs.update(
                {'url_prefix': settings.get('url_prefix') if settings.get('url_prefix') != "" else f"/{blueprint_name}"}
            )
            continue
        if setting in settings:
            if settings.get(setting, False):
                kwargs.update({setting: settings.get(setting)})

    return enabled, session, settings
