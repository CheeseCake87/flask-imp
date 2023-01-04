from flask import Flask, url_for


def loader(app: Flask):
    @app.route("/test-builtin")
    def t_import_builtins():
        return "success"

    @app.route("/test-structure")
    def t_import_structures():
        return url_for('theme.static', filename='img/Flask-BigApp-Logo.png')
