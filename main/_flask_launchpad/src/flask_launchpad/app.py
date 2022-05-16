from toml import load as toml_load
from flask import current_app
from flask import Blueprint
from importlib import import_module
from os import path
from os import listdir
from inspect import stack


def has_illegal_chars(name: str, exception: list = None) -> bool:
    """
    Removes illegal chars from dir, there are:
    ['%', '$', '£', ' ', '#', 'readme', '__', '.py']
    """
    _illegal_characters = ['%', '$', '£', ' ', '#', 'readme', '__', '.py']
    if exception is not None:
        for value in exception:
            _illegal_characters.remove(value)
    for char in _illegal_characters:
        if char in name:
            return True
    return False


class FlaskLaunchpad(object):
    def __init__(self, app=None):
        self._app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        if app is None:
            raise ImportError
        self._app = app

    def register_structure_folder(self, folder: str) -> None:
        """
        Registers a folder in the root path as a Flask template folder.
        :param folder: str
        :return: None
        """
        with self._app.app_context():
            structures = Blueprint(folder, folder, template_folder=f"{current_app.root_path}/{folder}")
            current_app.register_blueprint(structures)

    def app_config(self, file: str = None) -> None:
        """
        Enables the config.toml method to set Flask env vars, deal with custom Flask env vars,
        smtp settings, and database settings.
        """
        config = {}
        _file = file
        with self._app.app_context():
            if file is None:
                _file = "app_config.toml"

            if not path.isfile(f"{current_app.root_path}/{_file}"):
                raise ImportError("""
    Flask app has no valid config file, must be like app_config.toml and be in the root of the app.
                """)

            config.update(toml_load(f"{current_app.root_path}/{_file}"))

            if "flask" in config:
                for key, value in config["flask"].items():
                    current_app.config[key.upper()] = value
                del config["flask"]

            if "database" in config:
                database = config["database"]
                if "main" in database:
                    main_uri = database["main"]
                    if main_uri["type"] == "sqlite":
                        current_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:////{main_uri['database_name']}"
                    else:
                        type_user_pass = f"{main_uri['type']}://{main_uri['username']}:{main_uri['password']}"
                        server_database = f"@{main_uri['server']}/{main_uri['database_name']}"
                        current_app.config["SQLALCHEMY_DATABASE_URI"] = type_user_pass + server_database
                    del config["database"]["main"]

                current_app.config["SQLALCHEMY_BINDS"] = {}
                for key, value in config["database"].items():
                    if value["enabled"]:
                        type_user_pass = f"{value['type']}://{value['username']}:{value['password']}"
                        server_database = f"@{value['server']}/{value['database_name']}"
                        current_app.config["SQLALCHEMY_BINDS"].update({key: type_user_pass + server_database})
                del config["database"]

            if "smtp" in config:
                smtp = config["smtp"]
                current_app.config["SMTP"] = {}
                for key, value in smtp.items():
                    if value["enabled"]:
                        current_app.config["SMTP"].update({key: value})
                del config["smtp"]

            for key, value in config.items():
                current_app.config[key.upper()] = value

    def import_builtins(self, folder: str = "routes"):
        with self._app.app_context():
            routes_raw, routes_clean = listdir(f"{current_app.root_path}/{folder}"), []
            for route in routes_raw:
                if has_illegal_chars(route, exception=[".py"]):
                    continue
                routes_clean.append(route.replace(".py", ""))

            for route in routes_clean:
                try:
                    import_module(f"{folder.replace('/','.')}.{route}")
                except ImportError:
                    continue

    def import_blueprints(self, folder: str) -> None:
        """
        Looks through the passed in folder for Blueprint modules, imports them then registers them with Flask.
        The Blueprint object must be stored in a variable called bp in the __init__.py file on the Blueprint folder.
        :param folder: str
        :return: None
        """

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                if path.isdir(f"{current_app.root_path}/{folder}/{blueprint}"):
                    blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                _bp_root_folder = f"{current_app.root_path}/{folder}/{blueprint}"

                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}")
                    blueprint_object = getattr(blueprint_module, "bp")
                    current_app.register_blueprint(blueprint_object)
                except AttributeError as e:
                    print(e)
                    continue

                if path.isfile(f"{_bp_root_folder}/models.py"):
                    models_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}.models")
                    try:
                        import_object = getattr(models_module, "db")
                        import_object.init_app(current_app)
                    except AttributeError:
                        continue

    def import_apis(self, folder: str) -> None:
        """
        Looks through the passed in folder for Blueprint modules, imports them then registers them with Flask.
        This does the same as import_blueprints, but decorates the name with an api marker
        The Blueprint object must be stored in a variable called bp in the __init__.py file on the Blueprint folder.
        :param folder: str
        :return: None
        """

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                if path.isdir(f"{current_app.root_path}/{folder}/{blueprint}"):
                    blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                _bp_root_folder = f"{current_app.root_path}/{folder}/{blueprint}"

                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}")
                    blueprint_object = getattr(blueprint_module, "api_bp")
                    current_app.register_blueprint(blueprint_object)
                except AttributeError as e:
                    continue

                if path.isfile(f"{_bp_root_folder}/models.py"):
                    models_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}.models")
                    try:
                        import_object = getattr(models_module, "db")
                        import_object.init_app(current_app)
                    except AttributeError:
                        continue


class FLBlueprint:
    module_folder = None
    blueprint_name = None
    module_name = None
    config_file = "config.toml"
    this_config = None

    def __init__(self):
        caller = stack()[1]
        split_module_folder = caller.filename.split("/")[:-1]
        self.module_folder = "/".join(split_module_folder)
        self.blueprint_name = caller.filename.split("/")[-3:-2][0]
        self.module_name = caller.filename.split("/")[-2:-1][0]

    def config(self) -> dict:
        config = {}
        if not path.isfile(f"{self.module_folder}/{self.config_file}") or ".toml" not in self.config_file:
            raise ImportError("""
    Blueprint or API has no valid config file, must be like config.toml and be found in the root of the module.
                """)
        config.update(toml_load(f"{self.module_folder}/{self.config_file}"))
        return config

    def register(self, config_file: str = None):
        if config_file is not None:
            self.config_file = config_file
        self.this_config = self.config()
        settings = self.this_config["settings"]
        if "init" in self.this_config:
            if "enabled" in self.this_config["init"]:
                if not self.this_config["init"]["enabled"]:
                    return
            if "type" in self.this_config["init"]:
                if self.this_config["init"]["type"] == "api":
                    new_url = f"/{self.blueprint_name}{settings['url_prefix']}"
                    settings['url_prefix'] = new_url
        return Blueprint(self.module_name, self.module_name, **settings)

    def import_routes(self, folder: str = "routes"):
        routes_raw, routes_clean = listdir(f"{self.module_folder}/{folder}"), []
        for route in routes_raw:
            if has_illegal_chars(route, exception=[".py"]):
                continue
            routes_clean.append(route.replace(".py", ""))

        for route in routes_clean:
            try:
                import_module(f"{current_app.name}.{self.blueprint_name}.{self.module_name}.{folder}.{route}")
            except ImportError:
                continue
