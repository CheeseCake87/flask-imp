import logging
import os
import pathlib
from importlib import import_module
from inspect import stack
from typing import Dict, Union, Any

from flask import Blueprint
from flask import session
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

    def __init__(self, dunder_name, config_file: str = "config.toml") -> None:
        """
        dunder_name must be __name__
        config_file must be relative to the location of the blueprint.
        """
        self.location = pathlib.Path(stack()[1].filename).parent
        print(self.location.name)
        self.ba_name = self.location.parts[-1]
        self.package = dunder_name
        self.config = self.__load_config_file(config_file)

        super().__init__(self.ba_name, self.package, **self.__config_processor(self.config))

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

    def __config_processor(self, config: dict) -> dict:
        """
        Process the configuration file.
        """
        """Pull values from configuration dict"""
        self.enabled = config.get('enabled', False)
        self.session = config.get('session', {})
        settings = config.get('settings', {})

        __kwargs = dict()

        """Pull values from settings"""
        subdomain = settings.get('subdomain', False)
        url_defaults = settings.get('url_defaults', False)
        static_folder = settings.get('static_folder', False)
        template_folder = settings.get('template_folder', False)
        url_prefix = settings.get('url_prefix', False)
        upper_url_prefix = config.get('url_prefix', False)
        static_url_path = settings.get('static_url_path', False)

        """If values exist in the configuration file, set values"""
        if static_folder:
            __kwargs.update({'static_folder': static_folder})

        if template_folder:
            __kwargs.update({'template_folder': template_folder})

        if url_prefix:
            __kwargs.update({'url_prefix': url_prefix})

        if static_url_path:
            __kwargs.update({'static_url_path': static_url_path})

        if subdomain:
            __kwargs.update({'subdomain': subdomain})

        if url_defaults:
            __kwargs.update({'url_defaults': url_defaults})

        """If values get set to False, set defaults"""
        if static_folder is False:
            __kwargs.update({'static_folder': "static"})
            default_static_folder = self.location / "static"
            pathlib.Path.mkdir(default_static_folder, exist_ok=True)

        if template_folder is False:
            __kwargs.update({'template_folder': "templates"})
            default_template_folder = self.location / "templates"
            default_nested_template_folder = default_template_folder / self.location.name
            pathlib.Path.mkdir(default_template_folder, exist_ok=True)
            pathlib.Path.mkdir(default_nested_template_folder, exist_ok=True)

        if not __kwargs.get('url_prefix'):
            if upper_url_prefix:
                __kwargs.update({'url_prefix': f"/{upper_url_prefix}"})
            else:
                __kwargs.update({'url_prefix': f"/{self.location.name}"})

        if static_url_path is False:
            __kwargs.update({'static_url_path': f"/{self.location.name}/static"})

        return __kwargs
