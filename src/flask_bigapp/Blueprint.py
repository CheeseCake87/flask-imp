import logging
from flask import Blueprint
from flask import session
from inspect import stack
from jinja2 import Environment, FileSystemLoader
from os import listdir
from importlib import import_module

from .utilities import contains_illegal_chars
from .utilities import load_config, str_bool


class BigAppBlueprint(Blueprint):
    """
    Class that handles Blueprints from within the Blueprint __init__ file
    """
    enabled: bool = True
    name: str = str()
    config: dict = dict()
    session: dict = dict()
    location: str = str()

    import_location = None
    app_name_from_import = None
    nested_folder_from_import = None
    blueprint_name_from_import = None

    _loader: FileSystemLoader
    _env: Environment

    def __init__(self, dunder_name, config_file: str = "config.toml"):
        """
        dunder_name must be __name__
        """
        caller_stack = stack()[1]
        split_module_folder = caller_stack.filename.split("/")[:-1]
        self.location = "/".join(split_module_folder)

        self.import_location = dunder_name
        split_dunder_name = dunder_name.split(".")
        self.app_name_from_import = split_dunder_name[0]
        self.nested_folder_from_import = split_dunder_name[1]
        self.blueprint_name_from_import = split_dunder_name[2]

        self.name = self.blueprint_name_from_import

        self._process_config(config_file)

        self._loader = FileSystemLoader(f"{self.location}/{self.config['template_folder']}")
        self._env = Environment(loader=self._loader)

        super().__init__(self.name, self.import_location, **self.config)

    def _process_config(self, config_file) -> None:
        """
        Load the config file.
        """
        try:
            config_from_file = load_config(f"{self.location}/{config_file}")
        except FileNotFoundError:
            self.enabled = False
            logging.critical(f"{self.import_location} => Config file not found, skipping import.")
            return

        if "enabled" in config_from_file:
            if not str_bool(config_from_file["enabled"]):
                self.enabled = False
                return

        if "settings" not in config_from_file:
            self.enabled = False
            logging.critical(f"{self.import_location} => SETTINGS section is missing from config file.")
            return

        self.config.update(config_from_file["settings"])

        if "session" in config_from_file:
            self.session.update(config_from_file["session"])

        if "name" in config_from_file:
            self.name = config_from_file["name"]
            del config_from_file["name"]

        if "import_name" in config_from_file:
            logging.warning(
                f"{self.import_location} => import_name should not be define in config, this has been ignored.")
            del config_from_file["import_name"]

    def import_routes(self, folder: str = "routes"):
        """
        Imports all the routes in the given folder.

        If no folder is specified defaults to a folder named 'routes'
        """
        routes_raw, routes_clean = listdir(f"{self.location}/{folder}"), []
        for route in routes_raw:
            if contains_illegal_chars(route, exception=[".py"]):
                continue
            routes_clean.append(route.replace(".py", ""))

        for route in routes_clean:
            try:
                import_module(f"{self.import_name}.{folder}.{route}")
            except ImportError as e:
                logging.warning(f"Error when importing {self.import_name} - {self.name} - {route}: {e}")
                continue

    def init_session(self):
        """
        Initialize the session variables found in the config file.

        Use this method in the before_request route
        """
        for key in self.session:
            if key not in session:
                session.update(self.session)
                break

    def tmpl(self, template):
        """
        Pushes together the name of the blueprint and the template file to look for.

        This is a small time saving method to allow you to only type
        bp.tmpl("index.html") when looking for template files.
        """
        return f"{self.name}/{template}"
