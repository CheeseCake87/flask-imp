from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig, DatabaseConfig

bp = ImpBlueprint(
    __name__,
    ImpBlueprintConfig(
        enabled=True,
        url_prefix="/tests",
        template_folder="templates",
        static_folder="static",
        static_url_path="/tests/static",
        init_session={"tests_session": True},
        database_binds=[
            DatabaseConfig(
                enabled=False,
                bind_key="tests_db",
                database_name="tests_blueprint",
            )
        ],
    ),
)

bp.import_resources("routes")
bp.import_nested_blueprint("nested_test")
bp.import_nested_blueprints("group_of_nested")
bp.import_models("models")

print(":::-- tests nested bps", bp.nested_blueprints)
print(":::-- tests config id", id(bp.config))
