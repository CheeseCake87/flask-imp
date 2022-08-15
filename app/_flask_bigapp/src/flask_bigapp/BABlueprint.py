from flask import Blueprint


class BABlueprint(Blueprint):
    """
    Class that handles Blueprints from within the Blueprint __init__ file
    """
    enabled = True
    settings = dict()
    session = dict()
    location = str()

    def __init__(self, config_file: str = "config.toml"):
        from inspect import stack
        _caller = stack()[1]
        _split_module_folder = _caller.filename.split("/")[:-1]
        self.name = _caller.filename.split("/")[-2:-1][0]
        self.import_from = _caller.filename.split("/")[-3:-2][0]
        self.location = "/".join(_split_module_folder)
        bpn, bpi, bpa = self._process_config(config_file)
        super().__init__(bpn, bpi, **bpa)

    def _process_config(self, config_file):
        from .utilities import load_config, str_bool

        _config = load_config(f"{self.location}/{config_file}")
        _name = self.name

        if "settings" not in _config:
            raise ImportError(f"{self.import_from} => SETTINGS section is missing from config file.")

        self.settings.update(_config["settings"])

        if "session" in _config:
            self.session.update(_config["session"])

        if "enabled" in _config:
            if not str_bool(_config["enabled"]):
                self.enabled = False

        _strip_settings = self.settings.copy()

        if "name" in self.settings:
            del _strip_settings["name"]

        if "import_name" in self.settings:
            del _strip_settings["import_name"]

        return self.name, __name__, _strip_settings

    def import_routes(self, folder: str = "routes"):
        from os import listdir
        from importlib import import_module
        from flask import current_app
        from .utilities import contains_illegal_chars

        routes_raw, routes_clean = listdir(f"{self.location}/{folder}"), []
        for route in routes_raw:
            if contains_illegal_chars(route, exception=[".py"]):
                continue
            routes_clean.append(route.replace(".py", ""))

        for route in routes_clean:
            try:
                import_module(f"{current_app.name}.{self.import_from}.{self.name}.{folder}.{route}")
            except ImportError as e:
                print(f"""
Error when importing {self.import_from} - {self.name} - {route}: 
{e}
                """)
                continue

    def init_session(self):
        from flask import session
        for key in self.session:
            if key not in session:
                session.update(self.session)
                break
