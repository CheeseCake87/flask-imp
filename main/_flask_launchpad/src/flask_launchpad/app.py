from toml import load as toml_load
from flask import current_app
from flask import Blueprint
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from inspect import getmembers
from inspect import isclass
from sys import modules
from os import path
from os import listdir
from inspect import stack
from markupsafe import Markup

sql_do = SQLAlchemy().session


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


def load_config(root_path: str) -> dict:
    """
    This loads the config file of the Blueprint and saves it to the config var
    so it can be accessed using fl_bp.config
    """
    config = {}
    if not path.isfile(f"{root_path}/config.toml"):
        raise ImportError(f"""
Config file is invalid, must be config.toml and be found in the root of the module. Importing from {root_path}
            """)

    config.update(toml_load(f"{root_path}/config.toml"))

    return config


def model_class(class_name: str, app=None):
    """
    Returns a class object that is stored in app.config, returns error if not found.

    The shape of app.config["MODELS"] looks like this
    {
    "modules": { "module_name": {"import": "main.module.location", "io": import_object, "db": getattr("db") }, },
    "classes": { "class_name": class_object, }
    }
    """
    if app is None:
        app = current_app

    current_classes = app.config["MODELS"]["classes"]

    if class_name not in current_classes:
        raise KeyError(f"Model class {class_name} has not been found. Calling from {stack()[1]}")

    return current_classes[class_name]


def model_module(module_name: str, app=None) -> dict:
    """
    Returns

    The shape of app.config["MODELS"] looks like this
    {
    "modules": { "module_name": {"import": "main.module.location", "io": import_object, "db": getattr("db") }, },
    "classes": { "class_name": class_object, }
    }
    """
    if app is None:
        app = current_app

    current_models = app.config["MODELS"]

    if module_name not in current_models["modules"]:
        raise KeyError(f"Model module {module_name} has not been found. Calling from {stack()[1]}")

    return current_models["modules"][module_name]


class FlaskLaunchpad(object):
    """
    Main Flask-Launchpad Class
    """
    _app = None

    def __init__(self, app=None):
        """
        init method, fires init_app if app name is passed in. This is usually used when NOT using create_app()
        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        """
        init method used when working with create_app()
        """
        if app is None:
            raise ImportError("No app passed into the FlaskLaunchpad app")
        self._app = app

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

            current_app.config["MODELS"] = {"modules": {}, "classes": {}}
            current_app.config["SQLALCHEMY_BINDS"] = {}

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

    def import_builtins(self, folder: str = "routes") -> None:
        """
        This allows you to import app level routes and template_filters.
        It does the same as:
        from .routes import my_route
        But loops the import over all valid files found
        """
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
                    print("Error importing builtin: ", e, f"in {folder}/{route}")
                    continue

    def models_folder(self, folder: str) -> None:
        """
        This method is used to load valid model.py files into current_app.config["MODELS"]
        The shape of this data looks like this:
        app.config["MODELS"] {
        "modules": { "module_name": {"import": "main.module.location", "io": import_object, "db": getattr("db") }, },
        "classes": { "class_name": class_object, }
        }
        """
        with self._app.app_context():
            if not path.isdir(folder):
                folder = f"{current_app.root_path}/{folder}"
                if not path.isdir(folder):
                    print("Folder not found: ", folder)

            models_raw, modules_clean = listdir(folder), []

            for model in models_raw:
                if contains_illegal_chars(model, exception=[".py"]):
                    continue
                modules_clean.append(model.replace(".py", ""))

            models_files_dict = {}
            models_classes_dict = {}

            for model in modules_clean:
                split_folder = folder.split("/")
                strip_folder = split_folder[split_folder.index(current_app.name):]
                import_path = f"{'.'.join(strip_folder)}.{model}"
                try:
                    _model_module = import_module(import_path)
                    _model_object = getattr(_model_module, "db")

                except ImportError as e:
                    print("Error importing model: ", e, f" from {import_path}")
                    continue
                except AttributeError as e:
                    print("Error importing model: ", e, f" from {import_path}")
                    continue

                models_files_dict.update(
                    {model: {"import": import_path, "io": _model_module, "db": _model_object}})

                _model_object.init_app(current_app)

                model_members = getmembers(modules[import_path], isclass)
                for member in model_members:
                    class_name = member[0]
                    class_object = member[1]
                    if current_app.name in str(class_object):
                        models_classes_dict.update({class_name: class_object})

            current_app.config["MODELS"]["modules"].update(models_files_dict)
            current_app.config["MODELS"]["classes"].update(models_classes_dict)

    def create_all_models(self):
        """
        This creates the database, tables and fields from the models found in current_app.config["MODELS"]
        Can be used like:

        FlaskLaunchpad(current_app).create_all_models()

        ~or~

        create_app():
            ~~~~
            fl.create_all_models()
        """
        with self._app.app_context():
            for key, value in current_app.config["MODELS"]["modules"].items():
                SQLAlchemy.create_all(value["db"])

    def import_blueprints(self, folder: str) -> None:
        """
        Looks through the passed in folder for Blueprint modules; Imports them then registers them with Flask.
        The Blueprint object must be stored in a variable called bp in the __init__.py file in the Blueprint folder.
        """

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                _path = f"{current_app.root_path}/{folder}/{blueprint}"
                if path.isdir(_path):
                    if not contains_illegal_chars(blueprint):
                        if load_config(_path)["init"]["enabled"]:
                            blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                _bp_root_folder = f"{current_app.root_path}/{folder}/{blueprint}"

                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}")
                    blueprint_object = getattr(blueprint_module, "bp")
                    current_app.register_blueprint(blueprint_object)
                except AttributeError as e:
                    print("Error importing blueprint: ", e, f" from {_bp_root_folder}")
                    continue

    def import_apis(self, folder: str) -> None:
        """
        Looks through the passed in folder for Blueprint modules, imports them then registers them with Flask.
        This does the same as import_blueprints, but decorates the name with an api marker
        The Blueprint object must be stored in a variable called api_bp in the __init__.py file in the Api Blueprint folder.
        """

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                _path = f"{current_app.root_path}/{folder}/{blueprint}"
                if path.isdir(_path):
                    if not contains_illegal_chars(blueprint):
                        if load_config(_path)["init"]["enabled"]:
                            blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                _bp_root_folder = f"{current_app.root_path}/{folder}/{blueprint}"

                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}")
                    blueprint_object = getattr(blueprint_module, "api_bp")
                    current_app.register_blueprint(blueprint_object)
                except AttributeError as e:
                    print("Error importing api: ", e, f" from {_bp_root_folder}")
                    continue


class FLBlueprint:
    """
    Class that handles Blueprints from within the Blueprint __init__ file
    """
    module = None
    import_from = None
    root_path = None
    config_file = None
    config = None
    session = {}

    def __init__(self):
        """
        ini method sets defaults based on what file called the FLBlueprint Class.
        """
        caller = stack()[1]
        split_module_folder = caller.filename.split("/")[:-1]
        self.root_path = "/".join(split_module_folder)
        self.import_from = caller.filename.split("/")[-3:-2][0]
        self.name = caller.filename.split("/")[-2:-1][0]

    def register(self):
        """
        Pulls the settings from the Blueprints config file and uses them to register a Flask Blueprint.
        """
        self.config = load_config(self.root_path)

        try:
            c_init = self.config["init"]
            c_settings = self.config["settings"]
            c_blueprint = self.config["blueprint"]
        except KeyError:
            raise ImportError(f"{self.import_from} INIT and SETTINGS sections missing from config file.")

        if c_init["enabled"]:
            if c_settings["type"] == "api":
                new_url = f"/{self.import_from}{c_blueprint['url_prefix']}"
                c_settings['url_prefix'] = new_url

        if "session" in self.config:
            s = self.config["session"]
            for key, value in s.items():
                self.session[key] = value

        bp_name, bp_import_name = self.name, self.name

        if "name" in c_blueprint:
            bp_name = c_blueprint["name"]
            del c_blueprint["name"]

        if "import_name" in c_blueprint:
            bp_import_name = c_blueprint["import_name"]
            del c_blueprint["import_name"]

        if "template_folder" in c_blueprint:
            c_blueprint["template_folder"] = f"{self.root_path}/{c_blueprint['template_folder']}"

        return Blueprint(bp_name, bp_import_name, **c_blueprint)

    def import_routes(self, folder: str = "routes"):
        """
        Imports the routes from within the Blueprint folder.
        """
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


class FLStructure:
    _app = None
    _structures_folder = None
    _structures_absolute_folder = None
    _reg_structures = {}

    error_app_is_none = """
App has not been passed in. 
Do FLStructure(current_app, 'structure_being_used') 
or fls.init_app(app, 'structure_being_used')
    """

    error_structures_folder_is_none = """
Structure name has not been passed in. 
Do FLStructure(current_app, 'structure_being_used') 
or fls.init_app(app, 'structure_being_used')
    """

    def __init__(self, app=None, structures_folder: str = "structures"):
        if app is not None:
            self.init_app(app, structures_folder)

    def init_app(self, app=None, structures_folder: str = "structures"):
        if app is None:
            raise ImportError(self.error_app_is_none)

        self._app = app
        self._structures_folder = structures_folder
        with self._app.app_context():
            self._structures_absolute_folder = f"{current_app.root_path}/{self._structures_folder}"

    def register_structure(self, structure: str, template_folder: str = "templates",
                           static_folder: str = "static") -> None:
        """
        Registers a folder in the root path as a Flask template folder.
        The use of this is to allow for themes. I've called this structures and not themes as a template folder can
        import template files, macros, etc.
        """
        with self._app.app_context():
            t_folder = f"{current_app.root_path}/{self._structures_folder}/{structure}/{template_folder}"
            s_folder = f"{current_app.root_path}/{self._structures_folder}/{structure}/{static_folder}"
            if not path.isdir(t_folder):
                return
            if not path.isdir(s_folder):
                return
            structures = Blueprint(
                structure, structure,
                template_folder=t_folder, static_folder=s_folder, static_url_path=f"/{structure}/static/")
            current_app.register_blueprint(structures)
            self._reg_structures.update({
                structure: {"template_folder": t_folder, "static_folder": s_folder}
            })

    def extend(self, file: str, structure: str) -> str:
        p = f"{structure}/extends/{file}"
        if path.isfile(f"{self._reg_structures[structure]['template_folder']}/{p}"):
            return p
        return Markup(f"Extend template error, unable to find: {file} - extend > {p}")

    def include(self, file: str, structure: str) -> str:
        p = f"{structure}/includes/{file}"
        if path.isfile(f"{self._reg_structures[structure]['template_folder']}/{p}"):
            return p
        return Markup(f"Include template error, unable to find: {file} - include > {p}")

    def error_page(self, file: str, structure: str) -> str:
        p = f"{structure}/error_pages/{file}"
        if path.isfile(f"{self._reg_structures[structure]['template_folder']}/{p}"):
            return p
        return Markup(f"Error page render error, unable to find: {file} - error_page > {p}")

    def render(self, file: str, structure: str) -> str:
        p = f"{structure}/renders/{file}"
        if path.isfile(f"{self._reg_structures[structure]['template_folder']}/{p}"):
            return p
        return Markup(f"Page render error, unable to find: {file} - render > {p}")
