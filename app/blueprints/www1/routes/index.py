from flask import render_template

from app import bigapp
from flask_bigapp.security import api_login_check
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    example = bigapp.model("ExampleTable")
    example.get_first()

    return render_template(
        bp.tmpl("index.html")
    )


@bp.route("/api", methods=["GET"])
@api_login_check("logged_in")
def api():
    return {"request_success": True, "message": "Hello World"}
