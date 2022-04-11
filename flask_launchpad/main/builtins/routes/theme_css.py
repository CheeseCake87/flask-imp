from ..functions.utilities import is_file
from ..functions.utilities import get_app_root
from flask import send_from_directory
from flask import current_app


@current_app.route("/themes/<theme>/<filename>", methods=["GET"])
def theme_css(theme, filename):
    file_location = f"{get_app_root()}/templates/themes/{theme}/css"
    if is_file(f"{file_location}/{filename}"):
        return send_from_directory(
            directory=file_location,
            path=filename
        )
