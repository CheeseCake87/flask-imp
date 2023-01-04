from flask import Flask
from flask import render_template

theme = "theme"


def loader(app: Flask):
    @app.errorhandler(400)
    def system_400(error):
        render = f"{theme}/errors/400.html"
        return render_template(
            render,
        ), 400

    @app.errorhandler(401)
    def system_401(error):
        render = f"{theme}/errors/401.html"
        return render_template(
            render,
        ), 401

    @app.errorhandler(403)
    def system_403(error):
        render = f"{theme}/errors/403.html"
        return render_template(
            render,
        ), 403

    @app.errorhandler(404)
    def system_404(error):
        render = f"{theme}/errors/404.html"
        return render_template(
            render,
        ), 404

    @app.errorhandler(405)
    def system_405(error):
        render = f"{theme}/errors/405.html"
        return render_template(
            render,
        ), 405

    @app.errorhandler(500)
    def system_500(error):
        render = f"{theme}/errors/500.html"
        return render_template(
            render,
        ), 500
