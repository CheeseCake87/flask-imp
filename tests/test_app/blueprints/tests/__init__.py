from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")
bp.import_nested_blueprint("nested_test")
bp.import_nested_blueprints("group_of_nested")
bp.import_models("models")

print(":::-- tests nested bps", bp._nested_blueprints)
print(":::-- tests config id", id(bp.config))

@bp.before_app_request
def before_app_request():
    bp.init_session()
