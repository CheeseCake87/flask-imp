from flask_bigapp import Blueprint

page_needs = {
    "extend": "bigapp_default/extends/main.html",
    "footer": "bigapp_default/includes/footer.html",
}
bp = Blueprint(__name__)

bp.import_routes("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response
