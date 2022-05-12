from ..functions.utilities import is_file
from ..functions.utilities import get_app_root
from flask import send_from_directory
from flask import current_app


@current_app.route("/structures/<structure>/css/<filename>", methods=["GET"])
def structure_css(structure, filename):
    file_location = f"{get_app_root()}/structures/{structure}/css"
    if is_file(f"{file_location}/{filename}"):
        return send_from_directory(
            directory=file_location,
            path=filename
        )


@current_app.route("/structures/<structure>/js/<filename>", methods=["GET"])
def structure_js(structure, filename):
    file_location = f"{get_app_root()}/structures/{structure}/js"
    if is_file(f"{file_location}/{filename}"):
        return send_from_directory(
            directory=file_location,
            path=filename
        )


@current_app.route("/structures/<structure>/img/<filename>", methods=["GET"])
def structure_img(structure, filename):
    file_location = f"{get_app_root()}/structures/{structure}/img"
    if is_file(f"{file_location}/{filename}"):
        return send_from_directory(
            directory=file_location,
            path=filename
        )
