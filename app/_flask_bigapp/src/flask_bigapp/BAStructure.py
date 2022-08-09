class BAStructure:
    _app = None
    _structures_folder = None
    _structures_absolute_folder = None
    _reg_structures = {}

    error_app_is_none = """
App has not been passed in. 
Do BAStructure(current_app, 'structure_being_used') 
or bas.init_app(app, 'structure_being_used')
    """

    error_structures_folder_is_none = """
Structure name has not been passed in. 
Do FLStructure(current_app, 'structure_being_used') 
or bas.init_app(app, 'structure_being_used')
    """

    def __init__(self, app=None, structures_folder: str = "structures"):
        if app is not None:
            self.init_app(app, structures_folder)

    def init_app(self, app=None, structures_folder: str = "structures"):
        from flask import current_app

        if app is None:
            raise ImportError(self.error_app_is_none)

        self._app = app
        self._structures_folder = structures_folder
        with self._app.app_context():
            self._structures_absolute_folder = f"{current_app.root_path}/{self._structures_folder}"

    def register_structure(self, structure: str, template_folder: str = "templates", static_folder: str = "static") -> None:
        from os import path
        from flask import current_app, Blueprint

        with self._app.app_context():
            t_folder = f"{current_app.root_path}/{self._structures_folder}/{structure}/{template_folder}"
            s_folder = f"{current_app.root_path}/{self._structures_folder}/{structure}/{static_folder}"
            if not path.isdir(t_folder):
                return
            if not path.isdir(s_folder):
                return
            structures = Blueprint(
                structure, structure,
                template_folder=t_folder, static_folder=s_folder, static_url_path=f"/structure/{structure}")
            current_app.register_blueprint(structures)
            self._reg_structures.update({
                structure: {"template_folder": t_folder, "static_folder": s_folder}
            })

    @classmethod
    def extend(cls, file: str, structure: str) -> str:
        return f"{structure}/extends/{file}"

    @classmethod
    def include(cls, file: str, structure: str) -> str:
        return f"{structure}/includes/{file}"

    @classmethod
    def error_page(cls, file: str, structure: str) -> str:
        return f"{structure}/errors/{file}"

    @classmethod
    def render(cls, file: str, structure: str) -> str:
        return f"{structure}/renders/{file}"
