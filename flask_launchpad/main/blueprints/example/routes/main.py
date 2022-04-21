from .. import bp


@bp.route("/", methods=["GET"])
def index():
    """Example of route url redirect"""
    return """Working..."""
