from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(
    __name__,
    ImpBlueprintConfig(
        enabled=True,
        url_prefix="/self_reg",
        static_folder="static",
        template_folder="templates",
        init_session={"self_reg_session_loaded": True},
    ),
)

bp.import_resources("routes")
