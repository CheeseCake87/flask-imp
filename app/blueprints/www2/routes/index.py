from flask import render_template

from app.models.example_mixin import ExampleMixin
from app.models.example_table import ExampleTable
from flask_bigapp.security import login_check
from .. import bp
from ... import db


@bp.route("/", methods=["GET"])
def index():
    return render_template(
        bp.tmpl("index.html")
    )


@bp.route("/mixin", methods=["GET"])
def mixin_example():
    result = ExampleMixin.read(id_=1)
    ExampleTable.get_first()

    print(result)

    return "OK"


@bp.route("/login-test", methods=["GET"])
@login_check('logged_in', 'www.index', message="Test message")
def login_test():
    return render_template(
        bp.tmpl("index.html")
    )
