from typing import Literal
from os import path
from toml import load as toml_load


def contains_illegal_chars(name: str, exception: list = None) -> bool:
    """
    Checks if a string contains illegal characters.

    is able to handle exceptions
    """
    _illegal_characters = ['%', '$', '£', ' ', '#', 'readme', '__', '.py']
    if exception is not None:
        for value in exception:
            _illegal_characters.remove(value)
    for char in _illegal_characters:
        if char in name:
            return True
    return False


def load_config(config_path: str) -> dict:
    """
    Primarily used by BigAppBlueprint to load configuration files.
    """
    _config = {}
    _path = config_path

    if path.isfile(_path) and _path.endswith(".toml"):
        _config.update(toml_load(_path))
        return _config

    if not path.isfile(f"{_path}/config.toml"):
        raise ImportError(f"""
Config file is invalid, must be config.toml and be found in the root of the module. Importing from {_path}
            """)

    _config.update(toml_load(f"{_path}/config.toml"))

    return _config


def str_bool(bool_as_string: Literal["yes", "true", "1", "no", "false", "0"]) -> bool:
    """
    Checks if the passed in string is a boolean.
    """
    true = ["yes", "true", "1"]
    false = ["no", "false", "0"]
    if bool_as_string.lower() in true:
        return True
    if bool_as_string.lower() in false:
        return False
    raise ValueError(f"Invalid bool_as_string: {bool_as_string}")
