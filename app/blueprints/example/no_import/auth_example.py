from flask import render_template

from ...._flask_bigapp.src.flask_bigapp import auth
from app import structures

from .. import bp
from .. import stru


@bp.route("/auth-example", methods=["GET"])
def auth_example():
    render = "renders/auth-example.html"
    extend = structures.extend("main.html", stru)

    display_dict = {}

    display_dict.update({
        "auth.valid_email_chars()": auth.valid_email_chars()
    })

    return render_template(render, extend=extend, display_dict=display_dict)
