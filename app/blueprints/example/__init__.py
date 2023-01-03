from flask_bigapp import Blueprint

page_needs = {
    "extend": "default_theme/extends/main.html",
    "footer": "default_theme/includes/footer.html",
}
bp = Blueprint(__name__)

bp.import_routes("routes")

bp.import_nested_blueprint("example_nested")

bp.import_blueprint_models(folder="models")


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response
