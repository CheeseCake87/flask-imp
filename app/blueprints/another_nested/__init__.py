from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

config = ImpBlueprintConfig(
    enabled=True,
    url_prefix="/another_nested",
)

bp = ImpBlueprint(__name__, config)

bp.import_resources("routes")
bp.import_nested_blueprint("another_nested_two")
