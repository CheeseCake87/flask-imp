from flask import current_app
from flask import Blueprint
from os import path
from importlib import import_module

from .utilities.import_mgr import load_modules
from .utilities.import_mgr import read_config_as_dict
from .utilities.import_mgr import import_routes


class FlaskLaunchpad(object):
    _all = None

    def __init__(self, app=None):
        self._app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        if app is None:
            raise ImportError

        self._app = app

        print(app)

        structures = Blueprint(name="structures", import_name="structures",
                               template_folder=f"{app.root_path}/structures")
        app.register_blueprint(structures)

        # app.teardown_appcontext(self.teardown)

    def import_blueprints(self, folder: str):
        with self._app.app_context():
            for bp_name in load_modules(current_app.root_path, module_folder=folder):
                bp_root_folder = f"{current_app.root_path}/{folder}/{bp_name}"

                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder}.{bp_name}")
                    blueprint_object = getattr(blueprint_module, "bp")
                    current_app.register_blueprint(blueprint_object, name=f"{bp_name}")
                except AttributeError:
                    continue
                try:
                    for route in import_routes(current_app.root_path, module_folder=folder, module=bp_name):
                        import_module(f"{current_app.name}.{folder}.{bp_name}.routes.{route}")
                except ImportError:
                    continue

                if path.isfile(f"{bp_root_folder}/models.py"):
                    models_module = import_module(f"{current_app.name}.{folder}.{bp_name}.models")
                    try:
                        import_object = getattr(models_module, "db")
                        import_object.init_app(current_app)
                        bp_config = read_config_as_dict(current_app.root_path, module_folder=folder, module=bp_name)
                        if bp_config["init"]["share_models"]:
                            current_app.config["SHARED_MODELS"][bp_name] = import_object
                    except AttributeError:
                        continue

    # def connect(self):
    #     return sqlite3.connect(current_app.config['SQLITE3_DATABASE'])

    def teardown(self, exception):
        pass
        # ctx = _app_ctx_stack.top
        # if hasattr(ctx, 'sqlite3_db'):
        #     ctx.sqlite3_db.close()

    # @property
    # def connection(self):
    #     ctx = _app_ctx_stack.top
    #     if ctx is not None:
    #         if not hasattr(ctx, 'sqlite3_db'):
    #             ctx.sqlite3_db = self.connect()
    #         return ctx.sqlite3_db
