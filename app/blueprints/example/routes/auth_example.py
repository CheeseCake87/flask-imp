from flask import render_template

from app._flask_bigapp.src.flask_bigapp import Auth
from app import structures

from app.blueprints.example import bp
from app.blueprints.example import stru


@bp.route("/auth-example", methods=["GET"])
def auth_example():
    render = "renders/auth-example.html"
    extend = structures.extend("main.html", stru)

    display_dict = {}

    display_dict.update({
        "auth.valid_email_chars()": Auth.valid_email_chars()
    })

    return render_template(render, extend=extend, display_dict=display_dict)
