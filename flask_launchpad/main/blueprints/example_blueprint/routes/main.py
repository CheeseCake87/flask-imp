from ....builtins.functions.security import login_required
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return f"""example route"""


@bp.route("/this-page-is-locked", methods=["GET"])
def page_is_locked():
    return f"""This page is locked"""


@bp.route("/locked-page", methods=["GET"])
@login_required(on_error_endpoint="nothere")
def locked_page():
    return f"""On the locked page"""

