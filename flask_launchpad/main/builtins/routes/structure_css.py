from ..functions.utilities import is_file
from ..functions.utilities import get_app_root
from flask import send_from_directory
from flask import current_app


@current_app.route("/structures/<structure>/<filename>", methods=["GET"])
def structure_css(structure, filename):
    file_location = f"{get_app_root()}/builtins/templates/structures/{structure}/css"
    if is_file(f"{file_location}/{filename}"):
        return send_from_directory(
            directory=file_location,
            path=filename
        )
