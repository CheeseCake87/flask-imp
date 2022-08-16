from flask import Blueprint
from os import path
from inspect import stack


class BigAppBlueprint(Blueprint):
    """
    Class that handles Blueprints from within the Blueprint __init__ file
    """
    enabled = True
    settings = dict()
    session = dict()
    location = str()

    _app_name = None
    _nested_folder = None
    _blueprint_name = None
    _import_name = None

    def __init__(self, import_name, config_file: str = "config.toml"):
        _caller = stack()[1]
        _split_module_folder = _caller.filename.split("/")[:-1]
        _split_import_name = import_name.split(".")
        self.location = "/".join(_split_module_folder)
        self._import_name = import_name
        self._app_name = _split_import_name[0]
        self._nested_folder = _split_import_name[1]
        self._blueprint_name = _split_import_name[2]

        bpn, bps = self._process_config(config_file)
        super().__init__(bpn, self._import_name, **bps)

    def _process_config(self, config_file):
        from .utilities import load_config, str_bool

        _config = load_config(f"{self.location}/{config_file}")
        _name = self._blueprint_name

        if "settings" not in _config:
            raise ImportError(f"{self._import_name} => SETTINGS section is missing from config file.")

        self.settings.update(_config["settings"])

        if "session" in _config:
            self.session.update(_config["session"])

        if "enabled" in _config:
            if not str_bool(_config["enabled"]):
                self.enabled = False

        _strip_settings = self.settings.copy()

        if "name" in self.settings:
            _name = self.settings["name"]
            del _strip_settings["name"]

        if "import_name" in self.settings:
            del _strip_settings["import_name"]

        return _name, _strip_settings

    def import_routes(self, folder: str = "routes"):
        from os import listdir
        from importlib import import_module
        from .utilities import contains_illegal_chars

        routes_raw, routes_clean = listdir(f"{self.location}/{folder}"), []
        for route in routes_raw:
            if contains_illegal_chars(route, exception=[".py"]):
                continue
            routes_clean.append(route.replace(".py", ""))

        for route in routes_clean:
            try:
                import_module(f"{self._import_name}.{folder}.{route}")
            except ImportError as e:
                print(f"""
Error when importing {self._import_name} - {self.name} - {route}: 
{e}
                """)
                continue

    def init_session(self):
        from flask import session
        for key in self.session:
            if key not in session:
                session.update(self.session)
                break

    def _find_file(self, folder, file):
        if "template_folder" in self.settings:
            _nested = f"{self.location}/{self.settings['template_folder']}/{__name__}/{folder}/{file}"
            _rooted = f"{self.location}/{self.settings['template_folder']}/{folder}/{file}"
            if path.isfile(_nested):
                return f"{__name__}/{folder}/{file}"
            if path.isfile(_rooted):
                return f"{folder}/{file}"
            raise FileNotFoundError(f"{folder}/{file} cannot be found")
        raise KeyError(f"template_folder is not defined in the config of Blueprint: {__name__} ")

    def extend(self, file: str) -> str:
        return self._find_file("extends", file)

    def include(self, file: str) -> str:
        return self._find_file("includes", file)

    def errors(self, file: str) -> str:
        return self._find_file("errors", file)

    def render(self, file: str) -> str:
        return self._find_file("renders", file)
