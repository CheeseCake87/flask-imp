from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(
    __name__,
    ImpBlueprintConfig(
        enabled=True,
        url_prefix="/nested-test-two",
        static_url_path="/nested_test_two/static",
    ),
)

bp.import_resources("routes")
