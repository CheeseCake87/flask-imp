import functools
import logging
import re
from pathlib import Path
from typing import Union


def deprecated(message: str):
    logging.critical(f"Function deprecated: {message}")

    def func_wrapper(func):
        @functools.wraps(func)
        def proc_function(*args, **kwargs):
            return func(*args, **kwargs)

        return proc_function

    return func_wrapper


def cast_to_import_str(app_name: str, folder_path: Path) -> str:
    parts = folder_path.parts
    parts = parts[parts.index(app_name):]
    return ".".join(parts)


def class_field(class_: str, field: str) -> str:
    """
    Switches name of the class CamelCase to snake_case and tacks on the field name

    Used for SQLAlchemy foreign key assignments

    INFO ::: This function will not work if you are changing the __tablename__ of your model class
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_)
    snaked = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return f"{snaked}.{field}"


def cast_to_bool(value: Union[str, bool, None]) -> bool:
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
