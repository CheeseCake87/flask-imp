from toml import load as toml_load
from flask import current_app
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from sys import modules
from os import path
from os import listdir
from inspect import stack


def contains_illegal_chars(name: str, exception: list = None) -> bool:
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


# this function may not live long
def class_name_ok(class_name: str) -> bool:
    _banned_class_names = [
        "ForeignKey",
    ]
    if class_name in _banned_class_names:
        return False
    return True


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
                c_flask = config["flask"]
                if "static_folder" in c_flask:
                    current_app.static_folder = f"{current_app.root_path}/{c_flask['static_folder']}"
                    del config["flask"]["static_folder"]
                if "template_folder" in c_flask:
                    current_app.template_folder = f"{current_app.root_path}/{c_flask['template_folder']}"
                    del config["flask"]["template_folder"]

                for key, value in c_flask.items():
                    current_app.config[key.upper()] = value
                del config["flask"]

            current_app.config["models"] = {}

            if "database" in config:
                database = config["database"]
                if "main" in database:
                    main_uri = database["main"]
                    if main_uri["type"] == "sqlite":
                        current_app.config[
                            "SQLALCHEMY_DATABASE_URI"
                        ] = f"sqlite:////{current_app.root_path}/{main_uri['database_name']}.sqlite"
                    else:
                        type_user_pass = f"{main_uri['type']}://{main_uri['username']}:{main_uri['password']}"
                        server_database = f"@{main_uri['server']}/{main_uri['database_name']}"
                        current_app.config["SQLALCHEMY_DATABASE_URI"] = type_user_pass + server_database
                    del config["database"]["main"]

                current_app.config["SQLALCHEMY_BINDS"] = {}
                for key, value in config["database"].items():
                    if value["enabled"]:
                        if value["type"] == "sqlite":
                            database = f"sqlite:////{current_app.root_path}/{value['database_name']}.sqlite"
                            current_app.config["SQLALCHEMY_BINDS"].update({key: database})
                        else:
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
                if contains_illegal_chars(route, exception=[".py"]):
                    continue
                routes_clean.append(route.replace(".py", ""))

            for route in routes_clean:
                try:
                    import_module(f"{current_app.name}.{folder.replace('/', '.')}.{route}")
                except ImportError as e:
                    print(e)
                    continue

    def models_folder(self, folder: str, module: str = None) -> None:
        if not path.isdir(folder):
            return

        with self._app.app_context():
            if module is None:
                module = current_app.name

            models_raw, modules_clean = listdir(folder), []

            for model in models_raw:
                if contains_illegal_chars(model, exception=[".py"]):
                    continue
                modules_clean.append(model.replace(".py", ""))

            models_dict = {module: {}}

            for model in modules_clean:
                split_folder = folder.split("/")
                strip_folder = split_folder[split_folder.index(current_app.name):]
                import_path = f"{'.'.join(strip_folder)}.{model}"
                try:
                    model_module = import_module(import_path)
                    model_object = getattr(model_module, "db")
                except ImportError as e:
                    print(e)
                    continue
                except AttributeError as e:
                    print(e)
                    continue

                models_dict[module].update({model: {"import": model_module, "db": model_object, "classes": {}}})

                model_object.init_app(current_app)
                model_members = getmembers(modules[import_path], isclass)
                for member in model_members:
                    class_name = member[0]
                    class_object = member[1]
                    if current_app.name in str(class_object):
                        models_dict[module][model]["classes"].update({class_name: class_object})

            current_app.config["models"] = models_dict

    def create_all_models(self):
        with self._app.app_context():
            for key, value in current_app.config["models"].items():
                for ik, iv in value.items():
                    SQLAlchemy.create_all(iv["db"])

    def import_blueprints(self, folder: str) -> None:
        """
        Looks through the passed in folder for Blueprint modules, imports them then registers them with Flask.
        The Blueprint object must be stored in a variable called bp in the __init__.py file in the Blueprint folder.
        :param folder: str
        :return: None
        """

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                if path.isdir(f"{current_app.root_path}/{folder}/{blueprint}"):
                    if not contains_illegal_chars(blueprint):
                        blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                _bp_root_folder = f"{current_app.root_path}/{folder}/{blueprint}"

                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}")
                    blueprint_object = getattr(blueprint_module, "bp")
                    current_app.register_blueprint(blueprint_object)
                    fl_bp_object = getattr(blueprint_module, "fl_bp")
                    bp_settings = fl_bp_object.config["settings"]
                except AttributeError as e:
                    print("Error importing blueprint: ", e)
                    continue

                try:
                    self.models_folder(f"{_bp_root_folder}/{bp_settings['models_folder']}", blueprint)
                except KeyError as e:
                    print(e)

    def import_apis(self, folder: str) -> None:
        """
        Looks through the passed in folder for Blueprint modules, imports them then registers them with Flask.
        This does the same as import_blueprints, but decorates the name with an api marker
        The Blueprint object must be stored in a variable called api_bp in the __init__.py file in the Blueprint folder.
        :param folder: str
        :return: None
        """

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                if path.isdir(f"{current_app.root_path}/{folder}/{blueprint}"):
                    if not contains_illegal_chars(blueprint):
                        blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                _bp_root_folder = f"{current_app.root_path}/{folder}/{blueprint}"

                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}")
                    blueprint_object = getattr(blueprint_module, "api_bp")
                    current_app.register_blueprint(blueprint_object)
                    fl_bp_object = getattr(blueprint_module, "fl_bp")
                    bp_settings = fl_bp_object.config["settings"]
                except AttributeError as e:
                    continue

                if "models_folder" in bp_settings:
                    if path.isdir(f"{_bp_root_folder}/{bp_settings['models_folder']}"):
                        self.models_folder(f"{_bp_root_folder}/{bp_settings['models_folder']}", blueprint)

                if "model_folder" in bp_settings:
                    if path.isdir(f"{_bp_root_folder}/{bp_settings['model_folder']}"):
                        self.models_folder(f"{_bp_root_folder}/{bp_settings['model_folder']}", blueprint)


class FLBlueprint:
    module = None
    import_from = None
    root_path = None
    config_file = None
    config = None
    session = {}

    def __init__(self):
        caller = stack()[1]
        split_module_folder = caller.filename.split("/")[:-1]
        self.root_path = "/".join(split_module_folder)
        self.import_from = caller.filename.split("/")[-3:-2][0]
        self.name = caller.filename.split("/")[-2:-1][0]

    def load_config(self, config_file: str) -> dict:
        config = {}
        if not path.isfile(f"{self.root_path}/{config_file}") or ".toml" not in config_file:
            raise ImportError("""
    Blueprint or API has no valid config file, must be like config.toml and be found in the root of the module.
                """)

        config.update(toml_load(f"{self.root_path}/{config_file}"))
        self.config_file = config_file
        self.config = config

        return config

    def register(self, config_file: str = "config.toml"):
        config = self.load_config(config_file)

        try:
            c_init = config["init"]
            c_settings = config["settings"]
            c_blueprint = config["blueprint"]
        except KeyError:
            raise ImportError("INIT and SETTINGS sections missing from config file.")

        if c_init["enabled"]:
            if c_settings["type"] == "api":
                new_url = f"/{self.import_from}{c_blueprint['url_prefix']}"
                c_settings['url_prefix'] = new_url

        if "session" in config:
            s = config["session"]
            for key, value in s.items():
                self.session[key] = value

        bp_name, bp_import_name = self.name, self.name

        if "name" in c_blueprint:
            bp_name = c_blueprint["name"]
        else:
            self.config["name"] = self.name

        if "import_name" in c_blueprint:
            bp_import_name = c_blueprint["import_name"]
        else:
            self.config["import_name"] = self.name

        if "template_folder" in c_blueprint:
            c_blueprint["template_folder"] = f"{self.root_path}/{c_blueprint['template_folder']}"

        return Blueprint(bp_name, bp_import_name, **c_blueprint)

    def import_routes(self, folder: str = "routes"):
        routes_raw, routes_clean = listdir(f"{self.root_path}/{folder}"), []
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
