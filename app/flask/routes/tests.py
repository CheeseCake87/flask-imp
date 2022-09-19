from flask import current_app
from flask import url_for


@current_app.route("/test-builtin")
def t_import_builtins():
    return "success"


@current_app.route("/test-structure")
def t_import_structures():
    return url_for('bigapp_default.static', filename='img/Flask-BigApp-Logo.png')
