from .. import bp


@bp.route("/", methods=["GET"])
def index():
    """Example of route url redirect"""
    return """Working..."""


@bp.route("/test", methods=["GET"])
def test():
    """Example of route url redirect"""
    return """Working..."""
