from .. import bp


@bp.errorhandler(404)
def error_404(error):
    return "404 in blueprint", 404
