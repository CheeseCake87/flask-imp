from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(
    __name__,
    ImpBlueprintConfig(
        enabled=True,
    ),
)

bp.import_resources("routes")

print(":::-- from_object nested bps", bp.nested_blueprints)
print(":::-- from_object config id", id(bp.config))
