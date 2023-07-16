from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return "success"
