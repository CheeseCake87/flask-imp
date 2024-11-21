from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig, DatabaseConfig

bp = ImpBlueprint(
    __name__,
    ImpBlueprintConfig(
        enabled=True,
        url_prefix="/nested-test",
        template_folder="templates",
        database_binds=[
            DatabaseConfig(
                enabled=False,
                bind_key="nested_test_db",
                database_name="nested_test_database",
            )
        ],
    ),
)

bp.import_resources("routes")
bp.import_models("models")
