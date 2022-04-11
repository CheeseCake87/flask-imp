from .. import bp


"""
some example routes to test the route import of multiple files.
"""


@bp.route("/test1", methods=["GET"])
def test1():
    return f"""example route"""


@bp.route("/test2", methods=["GET"])
def test2():
    return f"""example route"""


@bp.route("/test3", methods=["GET"])
def test3():
    return f"""example route"""

