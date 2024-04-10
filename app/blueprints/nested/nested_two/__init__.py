from importlib.util import find_spec

from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")

print("-" * 80)
print(":::-- spec", find_spec(bp.package))
print(":::-- _nested_blueprints", bp._nested_blueprints, id(bp._nested_blueprints))
print("-" * 80)

# @bp.before_app_request
# def before_app_request():
#     bp.init_session()
