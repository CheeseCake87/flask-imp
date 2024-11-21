from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(
    __name__,
    ImpBlueprintConfig(
        enabled=True,
        url_prefix="//",
        init_session={"www_session_loaded": True},
    ),
)

bp.import_resources("routes")
bp.import_nested_blueprint("nested")
