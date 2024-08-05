from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

config = ImpBlueprintConfig(
    enabled=True,
    url_prefix="/nested",
)

bp = ImpBlueprint(__name__, config)

bp.import_resources("routes")
bp.import_nested_blueprint("nested_two")
