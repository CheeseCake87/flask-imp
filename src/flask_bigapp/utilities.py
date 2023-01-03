import functools
import logging
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
