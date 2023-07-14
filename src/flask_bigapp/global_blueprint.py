import logging
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from typing import Optional, Union, Protocol

import toml
from flask import Blueprint
from flask import session

from .helpers import init_bp_config
from .utilities import cast_to_import_str, deprecated


class BigApp(Protocol):
    ...


class BigAppGlobalBlueprint(Blueprint):
    """
    Class that handles Blueprints from within the Blueprint __init__ from_file
    """
    location: Path
    bp_name: str
    package: str
    overrides: dict

    _bigapp_instance: BigApp

    def __init__(self, dunder_name, static_url_path: str = "/"):
        """
        dunder_name must be __name__
        config_file must be relative to the location of the blueprint.
        """
        self.package = dunder_name
        self.app_name = dunder_name.split(".")[0]

        spec = find_spec(self.package)

        if spec is None:
            raise ImportError(f"Cannot find origin of {self.package}")

        self.location = Path(f"{spec.origin}").parent
        self.bp_name = self.location.name

        override_path = self.location / "overrides.toml"

        if override_path.exists():
            self.overrides = toml.load(override_path)

        super().__init__(
            self.bp_name,
            self.package,
            static_url_path=static_url_path
        )

        builtin_folders = (
            "context_processors",
            "error_handlers",
            "filters",
            "pre_post_request",
        )

        for folder in builtin_folders:

            route_path = self.location / folder
            if not route_path.exists():
                raise NotADirectoryError(f"{route_path} is not a directory")

            routes = route_path.glob("*.py")
            for route in routes:
                try:
                    import_module(f"{self.package}.{folder}.{route.stem}")
                except ImportError as e:
                    logging.warning(f"Error when importing {self.package}.{route}: {e}")
                    continue


