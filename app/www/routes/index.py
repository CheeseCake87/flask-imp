from flask import render_template
from flask_bigapp.security import login_check

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return render_template(
        bp.tmpl("index.html")
    )


@bp.route("/login-test", methods=["GET"])
@login_check('logged_in', 'www.index', message="Test message")
def login_test():
    return render_template(
        bp.tmpl("index.html")
    )
