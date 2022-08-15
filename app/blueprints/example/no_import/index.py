from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return "index route in example Blueprint"
