from flask import session
from .. import bp


"""
pre_post file is to hold the before and after blueprint settings. Can also call this file what you want.
pre_post.py is just shorter, but before_after_request.py makes more sense
"""

@bp.before_app_request
def before_app_request():
    if "auth" not in session:
        session['example1_auth'] = False
    pass


@bp.after_app_request
def after_app_request(response):
    return response
