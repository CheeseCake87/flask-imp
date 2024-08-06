from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(
    __name__,
    ImpBlueprintConfig(
        url_prefix="/root-blueprint", init_session={"root_blueprint_session": True}
    ),
)

bp.import_resources("routes")
