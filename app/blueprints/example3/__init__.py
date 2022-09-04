from flask_bigapp import Blueprint

bp = Blueprint(__name__)

page_needs = {
    "extend": "bigapp_default/extends/main.html",
    "footer": "bigapp_default/includes/footer.html",
}

bp.import_routes("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response
