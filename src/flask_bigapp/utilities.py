import functools
import logging
import os
import re
import sys
import typing as t
from pathlib import Path


class Sprinkles:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def deprecated(message: str):
    def func_wrapper(func):
        @functools.wraps(func)
        def proc_function(*args, **kwargs):
            logging.critical(f"{Sprinkles.FAIL}Function deprecated: {message}{Sprinkles.END}")
            return func(*args, **kwargs)

        return proc_function

    return func_wrapper


def if_env_replace(env_value: t.Optional[t.Any]) -> t.Any:
    """
    Looks for the replacement pattern to swap out values in the config from_file with environment variables.
    """
    pattern = re.compile(r'<(.*?)>')

    if isinstance(env_value, str):
        if re.match(pattern, env_value):
            env_var = re.findall(pattern, env_value)[0]
            return os.environ.get(env_var, "ENV_KEY_NOT_FOUND")
    return env_value


def capitalize_dict_keys(dictionary: t.Optional[dict]) -> dict:
    """
    Capitalizes the keys in a dictionary.
    """
    if dictionary is None:
        return {}

    return {key.upper(): value for key, value in dictionary.items()}


def lower_dict_keys(dictionary: t.Optional[dict]) -> dict:
    """
    Lowercases the keys in a dictionary.
    """
    if dictionary is None:
        return {}

    return {key.lower(): value for key, value in dictionary.items()}


def cast_to_import_str(app_name: str, folder_path: Path) -> str:
    folder_parts = folder_path.parts
    parts = folder_parts[folder_parts.index(app_name):]
    if sys.version_info.major == 3:
        if sys.version_info.minor < 9:
            return ".".join(parts).replace('.py', '')
        return ".".join(parts).removesuffix('.py')
    raise NotImplementedError("Python version not supported")


def snake(value: str) -> str:
    """
    Switches name of the class CamelCase to snake_case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def class_field(class_: str, field: str) -> str:
    """
    Switches name of the class CamelCase to snake_case and tacks on the field name

    Used for SQLAlchemy foreign key assignments

    INFO ::: This function may not produce the correct information if you are using __tablename__ in your class
    """
    return f"{snake(class_)}.{field}"


def cast_to_bool(value: t.Union[str, bool, None]) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        true_str = ("true", "yes", "y", "1")
        false_str = ("false", "no", "n", "0")

        if value.lower() in true_str:
            return True
        elif value.lower() in false_str:
            return False
        else:
            raise TypeError(f"Cannot cast {value} to bool")
    else:
        raise TypeError(f"Cannot cast {value} to bool")
