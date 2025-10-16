from ..helpers import strip_leading_slash


def api_blueprint_init_py(url_prefix: str, name: str) -> str:
    return f"""\
from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
    url_prefix="/{strip_leading_slash(url_prefix)}",
    init_session={{"{name}_session_loaded": True}},
))

bp.import_resources()
"""


def api_blueprint_resources_index_py() -> str:
    return """\
from flask_imp import ImpBlueprint

def include(bp: ImpBlueprint):
    @bp.route("/", methods=["GET"])
    def index():
        return {"message": "Hello, World!"}
"""
