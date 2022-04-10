from flask import current_app
from flask import request
from markupsafe import Markup


@current_app.route("/system/locked-page", endpoint="system.locked_page")
def locked_page():
    return """This page is locked."""


@current_app.route("/system/redirect-success", endpoint="system.redirect_success")
def redirect_success():
    return """A function has returned successful if you have been redirected here."""


@current_app.route("/system/redirect-catch-all", endpoint="system.redirect_catch_all")
def redirect_catch_all():
    re_var = """
    This is a redirect catch all.
    """
    if "tried" in request.args:
        re_var = f"""
        The endpoint: {request.args['tried']} does not exist
        """
    return Markup(re_var)
