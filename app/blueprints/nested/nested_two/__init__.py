from importlib.util import find_spec

from flask_imp import ImpBlueprint, ImpBlueprintConfig

config = ImpBlueprintConfig(
    enabled=True,
    url_prefix="/nested_two",
)

bp = ImpBlueprint(__name__, config)

bp.import_resources("routes")

print("-" * 80)
print(":::-- spec", find_spec(bp.package))
print(":::-- _nested_blueprints", bp._nested_blueprints, id(bp._nested_blueprints))
print("-" * 80)

# @bp.before_app_request
# def before_app_request():
#     bp.init_session()
