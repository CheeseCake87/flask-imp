import functools
import logging
import re
import sys
import typing as t
from pathlib import Path

from flask import Flask

from .protocols import DatabaseConfig, Imp


class Sprinkles:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


_toml_suffix = (".toml", ".tml")


def deprecated(message: str) -> t.Callable[[t.Any], t.Any]:
    def func_wrapper(func: t.Any) -> t.Any:
        @functools.wraps(func)
        def proc_function(*args: t.Any, **kwargs: t.Any) -> t.Any:
            logging.warning(
                f"{Sprinkles.FAIL}Function deprecated: {message}{Sprinkles.END}"
            )
            return func(*args, **kwargs)

        return proc_function

    return func_wrapper


def _partial_models_import(
    location: Path,
    file_or_folder: str,
    imp_instance: Imp,
) -> None:
    file_or_folder_path = Path(location / file_or_folder)
    imp_instance.import_models(f"{file_or_folder_path}")


def _partial_database_binds(
    imp_instance: Imp,
    database_bind: t.Union[t.Any, DatabaseConfig],
) -> None:
    if "SQLALCHEMY_BINDS" in imp_instance.app.config:
        imp_instance.app.config["SQLALCHEMY_BINDS"][database_bind.bind_key] = (
            build_database_uri(imp_instance.app, imp_instance.app_path, database_bind)
        )
    else:
        imp_instance.app.config["SQLALCHEMY_BINDS"] = {
            database_bind.bind_key: build_database_uri(
                imp_instance.app, imp_instance.app_path, database_bind
            )
        }


def build_database_main(
    flask_app: Flask,
    app_instance_path: Path,
    database_main: t.Optional[DatabaseConfig] = None,
) -> None:
    if database_main:
        if database_main.enabled:
            flask_app.config["SQLALCHEMY_DATABASE_URI"] = build_database_uri(
                flask_app, app_instance_path, database_main
            )


def build_database_binds(
    flask_app: Flask,
    app_instance_path: Path,
    database_binds: t.Optional[t.Iterable[DatabaseConfig]] = None,
) -> None:
    if database_binds:
        for db in database_binds:
            if db.enabled:
                if "SQLALCHEMY_BINDS" not in flask_app.config:
                    flask_app.config["SQLALCHEMY_BINDS"] = {}

                flask_app.config["SQLALCHEMY_BINDS"][db.bind_key] = build_database_uri(
                    flask_app, app_instance_path, db
                )


def build_database_uri(
    flask_app: Flask, app_instance_path: Path, db: DatabaseConfig
) -> str:
    if db.dialect == "sqlite":
        filepath = app_instance_path / (
            db.name + flask_app.config.get("SQLITE_DB_EXTENSION", ".sqlite")
        )
        return f"{db.dialect}:///{filepath}"

    return (
        f"{db.dialect}://{db.username}:"
        f"{db.password}@{db.location}:"
        f"{db.port}/{db.name}"
    )


def cast_to_import_str(app_name: str, folder_path: Path) -> str:
    """
    Takes the folder path and converts it to a string that can be imported
    """
    folder_parts = folder_path.parts
    parts = folder_parts[folder_parts.index(app_name) :]
    if sys.version_info.major == 3:
        if sys.version_info.minor < 9:
            return ".".join(parts).replace(".py", "")
        return ".".join(parts).removesuffix(".py")
    raise NotImplementedError("Python version not supported")


def snake(value: str) -> str:
    """
    Switches name of the class CamelCase to snake_case
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", value)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def slug(value: str) -> str:
    """
    Switches name of the class CamelCase to slug-case
    """
    value = value.replace("_", "-")
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", value)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower()


def class_field(class_: str, field: str) -> str:
    """
    Switches name of the class CamelCase to snake_case and tacks on the field name

    Used for SQLAlchemy foreign key assignments

    INFO ::: This function may not produce the correct information if you are using __tablename__ in your class
    """
    return f"{snake(class_)}.{field}"


def cast_to_bool(value: t.Union[str, bool, None]) -> bool:
    """
    Casts an array of truly string values to a boolean. Used for config files.
    """
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


def cast_to_int(value: t.Union[str, int, float, bool, None]) -> int:
    """
    Casts string, float, and bool to int
    """

    if value is None:
        return 0

    if isinstance(value, int):
        return value

    if isinstance(value, str):
        if value == "":
            return 0

        try:
            return int(value)
        except ValueError:
            raise TypeError(f"Cannot cast {value} to int")

    if isinstance(value, float):
        return int(value)

    if isinstance(value, bool):
        if value:
            return 1
        return 0

    raise TypeError(f"Cannot cast {value} to int")


def cast_to_float(value: t.Union[str, int, float, bool, None]) -> float:
    """
    Casts string, int, and bool to float
    """

    if value is None:
        return 0.0

    if isinstance(value, float):
        return value

    if isinstance(value, str):
        if value == "":
            return 0.0

        try:
            return float(value)
        except ValueError:
            raise TypeError(f"Cannot cast {value} to float")

    if isinstance(value, int):
        return float(value)

    if isinstance(value, bool):
        if value:
            return 1.0
        return 0.0

    raise TypeError(f"Cannot cast {value} to float")
