from ..functions.structure import StructureBuilder
from flask import current_app
from flask import Response
from flask import session
from flask import request
from flask import render_template
from markupsafe import Markup

struc = StructureBuilder(current_app.config["STRUCTURE"])


@current_app.errorhandler(404)
def request_404(error):
    render = struc.error("404.html")
    structure = struc.name()
    return render_template(
        render,
        structure=structure,
        path=request.path
    ), 404


@current_app.errorhandler(401)
def custom_401(error):
    return Response('You are unauthorized to access this resource.', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


@current_app.route("/errors/redirect-catch-all", endpoint="errors.redirect_catch_all")
def redirect_catch_all():
    render = struc.error("redirect_catch_all.html")
    structure = struc.name()
    endpoint_tried = ""
    if "tried" in request.args:
        endpoint_tried = f"The endpoint: {request.args['tried']} does not exist"
    return render_template(
        render,
        structure=structure,
        path=request.path,
        endpoint=request.args['tried'],
        endpoint_tried=endpoint_tried
    ), 404
