from flask import Flask


def test_factory(app: Flask):
    app.route("/factory")(lambda: "Hello, Test Factory!")
