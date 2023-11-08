from flask import Blueprint

bp = Blueprint("regular_blueprint", __name__)


@bp.route("/regular-blueprint")
def regular_blueprint():
    return "regular_blueprint"
