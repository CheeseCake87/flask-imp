import logging
import pathlib
import os

from flask import Blueprint
from flask import session
from inspect import stack
from typing import Dict, Union, Any
from importlib import import_module
from toml import load


class BigAppBlueprint(Blueprint):
    """
    Class that handles Blueprints from within the Blueprint __init__ file
    """
    enabled: bool = False
    location: pathlib.Path
    ba_name: str
    package: str
    config: dict
    session: dict

    __kwargs: dict

    def __init__(self, dunder_name, config_file: str = "config.toml") -> None:
        """
        dunder_name must be __name__
        config_file must be relative to the location of the blueprint.
        """
        self.location = pathlib.Path(stack()[1].filename).parent
        self.ba_name = self.location.parts[-1]
        self.package = dunder_name
        self.config = self.__load_config_file(config_file)
        self.__config_processor(self.config)

        super().__init__(self.ba_name, self.package, **self.__kwargs)

    def import_routes(self, folder: str = "routes") -> None:
        """
        Imports all the routes in the given folder.
        If no folder is specified defaults to a folder named 'routes'

        Folder must be relative ( folder="here" not folder="/home/user/app/folder/blueprint/folder" )
        """
        path = self.location / folder
        if not path.exists():
            raise NotADirectoryError(f"{path} is not a directory")

        routes = path.glob("*.py")
        for route in routes:
            try:
                import_module(f"{self.package}.{folder}.{route.stem}")
            except ImportError as e:
                logging.warning(f"Error when importing {self.package}.{route}: {e}")
                continue

    def init_session(self) -> None:
        """
        Initialize the session variables found in the config file.
        Use this method in the before_request route.
        """
        for key in self.session:
            if key not in session:
                session.update(self.session)
                break

    def tmpl(self, template) -> str:
        """
        Pushes together the name of the blueprint and the template file to look for.
        This is a small time saving method to allow you to only type
        bp.tmpl("index.html") when looking for template files.
        """
        return f"{self.name}/{template}"

    def __load_config_file(self, config_file: Union[Any, os.PathLike]) -> Dict:
        """
        Attempts to load the configuration file.
        """
        config_suffix = ('.toml', '.tml')

        if config_file is None:
            raise ImportError(f"The Blueprint {self.package} config file cannot be None!")

        config_path: pathlib.PurePath = pathlib.PurePath(self.location / config_file)

        if not pathlib.Path(config_path).exists():
            raise ImportError(f"The Blueprint {self.package} config file does not exist!")

        if config_path.suffix not in config_suffix:
            raise ImportError(f"The Blueprint {self.package} config file must be a toml file!")

        return load(config_path)

    def __config_processor(self, config: dict) -> None:
        """
        Process the configuration file.
        """
        self.enabled = config.get('enabled', False)
        self.__kwargs = config.get('settings', None)
        self.session = config.get('session', {})
        if self.__kwargs is None:
            raise ImportError(f"The Blueprint {self.package} is missing the settings section")
