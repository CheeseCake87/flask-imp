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
    if app is None:
        app = current_app

    current_classes = app.config["models"]["classes"]

    if class_name not in current_classes:
        return print(f"Model class {class_name} has not been found.")

    return current_classes[class_name]


def model_module(module_name: str, app=None) -> dict:
    if app is None:
        app = current_app

    current_models = app.config["models"]

    if module_name not in current_models["modules"]:
        raise KeyError(f"Model module {module_name} has not been found.")

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

            current_app.config["structure_folders"] = {}
            current_app.config["models"] = {"modules": {}, "classes": {}}
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

    def register_structure_folder(self, folder: str) -> None:
        """
        Registers a folder in the root path as a Flask template folder.
        The use of this is to allow for themes. I've called this structures and not themes as a template folder can
        import template files, macros, etc.
        """
        with self._app.app_context():
            structures = Blueprint(folder, folder, template_folder=f"{current_app.root_path}/{folder}")
            current_app.register_blueprint(structures)
            current_app.config["structure_folder"] = f"{current_app.root_path}/{folder}"

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
                    print(e)
                    continue

    def models_folder(self, folder: str) -> None:
        """
        This method is used to load valid model.py files into current_app.config["models"]
        The shape of this data looks like this:
        { module (blueprint name / app name):
            { model (name of model file):
                "import": <the import of the file>,
                "classes": { class_name (name of the class in the model file): class_object (the class itself)
            }
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
                    print("Error importing model: ", e)
                    continue
                except AttributeError as e:
                    print("Error importing model: ", e)
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

            current_app.config["models"]["modules"].update(models_files_dict)
            current_app.config["models"]["classes"].update(models_classes_dict)

    def create_all_models(self):
        """
        This creates the database, tables and fields from the models found in current_app.config["models"]
        Can be used like:

        FlaskLaunchpad(current_app).create_all_models()

        ~or~

        create_app():
            ~~~~
            fl.create_all_models()
        """
        with self._app.app_context():
            for key, value in current_app.config["models"]["modules"].items():
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
                    print("Error importing blueprint: ", e)
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
            raise ImportError("INIT and SETTINGS sections missing from config file.")

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
    _sn = None
    _sf = None
    _sp = None
    _app = None

    def __init__(self, app=None, structure_name: str = None):
        if app is None:
            raise ImportError(
                "App has not been passed in. Do FLStructure(current_app, 'structure_being_used')")

        if structure_name is None:
            raise ImportError(
                "Structure name has not been passed in. Do FLStructure(current_app, 'structure_being_used')")

        self._app = app
        self._sn = structure_name

        with self._app.app_context():
            if "structure_folder" not in current_app.config:
                raise ImportError(
                    "Structure folder has not been registered. Do fl.register_structure_folder('folder_that_contains_structures')")

            self._sf = current_app.config["structure_folder"]
            self._sp = f"{self._sf}/{self._sn}"

    def extend(self, extending: str) -> str:
        """
        Looks for the template to extend in the specified structure.
        """
        if path.isfile(f"{self._sp}/extends/{extending}"):
            return f"{self._sn}/extends/{extending}"
        return Markup(f"Extend template error, unable to find: {extending}")

    def include(self, including: str) -> str:
        """
        Looks for the file to be included in the page.
        """
        if path.isfile(f"{self._sp}/includes/{including}"):
            return f"{self._sn}/includes/{including}"
        return Markup(f"Include template error, unable to find: {including}")

    def error(self, error_page: str) -> str:
        """
        Checks if an error page location exists and if so returns its location valid with Flask template folders.
        To use do.

        in Builtin error routes:
        fls = FLStructure(current_app, "structure_name")
        / structure_name is the folder name of a structure /

        in Blueprint route:
        render_template(fls.error("error_page.html))
        / checks for file in folder structure_name/error_pages/error_page.html /
        """
        if path.isfile(f"{self._sp}/error_pages/{error_page}"):
            return f"{self._sn}/error_pages/{error_page}"
        return Markup(f"Error page render error, unable to find: {error_page}")

    def render(self, render_page: str) -> str:
        """
        Checks if a render page location exists and if so returns its location valid with Flask template folders.
        To use do.

        in Blueprint init:
        fls = FLStructure(current_app, "structure_name")
        / structure_name is the folder name of a structure /

        in Blueprint route:
        render_template(fls.render("page.html))
        / checks for file in folder structure_name/renders/page.html /
        """
        if path.isfile(f"{self._sp}/renders/{render_page}"):
            return f"{self._sn}/renders/{render_page}"
        return Markup(f"Page render error, unable to find: {render_page}")

    def name(self) -> str:
        """
        Simply returns the name of the structure
        """
        return self._sn
