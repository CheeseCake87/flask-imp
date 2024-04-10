from flask_imp import Blueprint

bp = Blueprint(__name__, "config_from_object.Config")

bp.import_resources("routes")

print(":::-- from_object nested bps", bp._nested_blueprints)
print(":::-- from_object config id", id(bp.config))

@bp.before_app_request
def before_app_request():
    bp.init_session()
