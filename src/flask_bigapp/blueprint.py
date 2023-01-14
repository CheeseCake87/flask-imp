import logging
from importlib import import_module
from importlib.util import find_spec
from inspect import getmembers, isclass
from pathlib import Path
from types import ModuleType
from typing import Dict, Optional, Union

from flask import Blueprint
from flask import session
from toml import load as toml_load

from flask_bigapp.utilities import cast_to_bool, cast_to_import_str, deprecated


class BigAppBlueprint(Blueprint):
    """
    Class that handles Blueprints from within the Blueprint __init__ from_file
    """
    enabled: bool = False
    location: Path
    bp_name: str
    package: str
    session: dict

    nested_blueprints: Dict[str, Optional[ModuleType]]

    def __init__(self, dunder_name, config_file: str = "config.toml"):
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

        self.nested_blueprints = {}

        bp_args = self._init_bp_config(Path(self.location / config_file)) or {}

        super().__init__(
            self.bp_name,
            self.package,
            **bp_args
        )

    def import_routes(self, folder: str = "routes") -> None:
        """
        Imports all the routes in the given from_folder.
        If no from_folder is specified defaults to a from_folder named 'routes'

        Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder/blueprint/from_folder" )
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

    def import_nested_blueprints(self, folder: str) -> None:
        """
        Imports all the blueprints in the given from_folder.

        Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """

        folder_path = Path(self.location / folder)

        for potential_bp in folder_path.iterdir():
            self.import_nested_blueprint(potential_bp)

    def import_nested_blueprint(self, blueprint: Union[str, Path]):
        """
        Imports a single blueprint from the given path.

        Path must be relative ( path="here" not path="/home/user/app/from_folder" )
        """
        if isinstance(blueprint, str):
            potential_bp = Path(self.location / blueprint)
        else:
            potential_bp = blueprint

        if potential_bp.is_dir():
            if potential_bp.name in self.nested_blueprints:
                raise ImportError(
                    f"Nested blueprint {potential_bp.name} is already registered, blueprint folders must be unique\n"
                    f"Importing from {potential_bp}"
                )
            app_name = self.package.split(".")[0]
            try:
                module = import_module(cast_to_import_str(app_name, potential_bp))
                for dir_item in dir(module):
                    _ = getattr(module, dir_item)
                    if isinstance(_, BigAppBlueprint):
                        if _.enabled:
                            self.nested_blueprints.update(
                                {potential_bp.name: module}
                            )
                            self.register_blueprint(_)
                        break
            except Exception as e:
                logging.critical(f"{e}\n", f"Error importing blueprint: from {potential_bp}")

    def init_session(self) -> None:
        """
        Initialize the session variables found in the config from_file.
        Use this method in the before_request route.
        """
        for key in self.session:
            if key not in session:
                session.update(self.session)
                break

    @deprecated("import_blueprint_models() is deprecated Use import_models instead")
    def import_blueprint_models(
            self,
            from_file: Optional[str] = None,
            from_folder: Optional[str] = None
    ) -> None:
        self.import_models(from_file=from_file, from_folder=from_folder)

    def import_models(
            self,
            from_file: Optional[str] = None,
            from_folder: Optional[str] = None
    ) -> None:
        """
        Imports model files from a single from_file or a from_folder. Both are allowed to be set.

        File and Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """
        from flask_bigapp import BigApp

        def get_bigapp_instance() -> BigApp:
            app_module = import_module(self.app_name)
            for dir_item in dir(app_module):
                potential_instance = getattr(app_module, dir_item)
                if isinstance(potential_instance, BigApp):
                    return potential_instance
            raise ImportError(f"Cannot find BigApp instance in {self.app_name}")

        bigapp_instance = get_bigapp_instance()

        if isinstance(from_file, str):
            from_file = Path(self.location / from_file)

        if isinstance(from_folder, str):
            from_folder = Path(self.location / from_folder)

        bigapp_instance.import_models(from_file, from_folder)

    def tmpl(self, template) -> str:
        """
        Pushes together the name of the blueprint and the template from_file to look for.
        This is a small-time saving method to allow you to only type
        bp.tmpl("index.html") when looking for template files.
        """
        return f"{self.name}/{template}"

    def _init_bp_config(self, config_file_path) -> Optional[dict]:
        """
        Attempts to load the and process the configuration from_file.
        """

        if not config_file_path.exists():
            raise FileNotFoundError(f"{self.bp_name} Blueprint config from_file {config_file_path.name} was not found")

        config_suffix = ('.toml', '.tml')

        if config_file_path.suffix not in config_suffix:
            raise TypeError(f"Config from_file must be one of the following types: {config_suffix}")

        config = toml_load(config_file_path)

        self.enabled = cast_to_bool(config.get('enabled', False))
        self.session = config.get('session', {})
        settings = config.get('settings', {})

        kwargs = dict()

        """Pull values from settings"""
        url_prefix = settings.get('url_prefix', "")
        subdomain = settings.get('subdomain', "")
        url_defaults = settings.get('url_defaults', dict())
        static_folder = settings.get('static_folder', "")
        template_folder = settings.get('template_folder', "")
        static_url_path = settings.get('static_url_path', "")
        root_path = settings.get('root_path', "")

        """If values exist in the configuration from_file, set values"""
        kwargs.update({'url_prefix': url_prefix if url_prefix != "" else f"/{self.bp_name}"})

        if subdomain:
            kwargs.update({'subdomain': subdomain})

        if url_defaults:
            kwargs.update({'url_defaults': url_defaults})

        if static_folder:
            kwargs.update({'static_folder': static_folder})

        if template_folder:
            kwargs.update({'template_folder': template_folder})

        if static_url_path:
            kwargs.update({'static_url_path': static_url_path})

        if root_path:
            kwargs.update({'root_path': root_path})

        return kwargs
