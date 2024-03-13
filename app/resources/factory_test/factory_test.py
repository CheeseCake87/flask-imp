from flask import Flask


def factory_in_folder(app: Flask):
    app.route("/factory")(lambda: "Hello, Test Factory!")
