from flask import abort


def include(bp):
    @bp.route("/error-page-404", methods=["GET"])
    def error_page_404():
        return abort(404)

    @bp.route("/error-page-500", methods=["GET"])
    def error_page_500():
        return abort(500)
