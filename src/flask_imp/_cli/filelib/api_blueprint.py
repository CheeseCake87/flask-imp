def api_blueprint_init_py(url_prefix: str, name: str) -> str:
    return f"""\
from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
    url_prefix="/{url_prefix}",
    init_session={{"{name}_session_loaded": True}},
))

bp.import_resources("routes")
"""


def api_blueprint_routes_index_py() -> str:
    return """\
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return {"message": "Hello, World!"}
"""
