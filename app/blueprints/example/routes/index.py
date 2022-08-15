from app.blueprints.example import bp


@bp.route("/", methods=["GET"])
def index():
    return "index route in example Blueprint"
