from os import listdir
from os import path
from flask import Blueprint
from flask import current_app


class Structures:
    structures = dict()

    def import_structures(self, flask_app, structures_folder: str) -> None:
        from .utilities import contains_illegal_chars

        with flask_app.app_context():
            structures_raw, structures_clean = listdir(f"{flask_app.root_path}/{structures_folder}/"), []
            dunder_name = __name__
            split_dunder_name = dunder_name.split(".")

            for structure in structures_raw:
                _path = f"{flask_app.root_path}/{structures_folder}/{structure}"
                if path.isdir(_path):
                    if not contains_illegal_chars(structure):
                        structures_clean.append(structure)

            for structure in structures_clean:
                _structure_root_folder = f"{flask_app.root_path}/{structures_folder}/{structure}"
                self.structures.update({structure: _structure_root_folder})
                bp = Blueprint(
                    name=structure,
                    import_name=f"{split_dunder_name[0]}/{structures_folder}/{structure}",
                    static_folder=f"{flask_app.root_path}/{structures_folder}/{structure}/static",
                    template_folder=f"{flask_app.root_path}/{structures_folder}/{structure}/templates",
                    static_url_path=f"/{structure}/static"
                )
                current_app.register_blueprint(bp)

    @staticmethod
    def tmpl(structure, template):
        return f"{structure}/{template}"
