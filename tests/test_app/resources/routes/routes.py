from flask import Flask
from flask import render_template


def collection(app: Flask):
    @app.route("/")
    def index():
        return render_template(
            "index.html",
        )
