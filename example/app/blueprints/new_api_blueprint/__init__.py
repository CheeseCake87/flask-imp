from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(
    __name__,
    ImpBlueprintConfig(
        enabled=True,
        url_prefix="/new_api_blueprint",
        init_session={"new_api_blueprint_session_loaded": True},
    ),
)

bp.import_resources("routes")
