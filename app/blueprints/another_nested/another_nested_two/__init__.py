from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig, DatabaseConfig

config = ImpBlueprintConfig(
    enabled=True,
    url_prefix="/another_nested_two",
    database_binds=[
        DatabaseConfig(
            enabled=True,
            dialect="sqlite",
            name="another_nested_two",
            bind_key="another_nested_two",
        )
    ]
)

bp = ImpBlueprint(__name__, config)

bp.import_resources("routes")
