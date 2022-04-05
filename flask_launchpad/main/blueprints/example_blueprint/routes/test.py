from .. import bp


@bp.route("/test1", methods=["GET"])
def test1():
    return f"""example route"""


@bp.route("/test2", methods=["GET"])
def test2():
    return f"""This page is locked"""


@bp.route("/test3", methods=["GET"])
def test3():
    return f"""On the locked page"""

