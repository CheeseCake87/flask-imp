def resources_cli_py() -> str:
    return """\
from flask import Flask


def include(app: Flask):
    @app.cli.command("show-config")
    def show_config():
        print(app.config)
"""


def resources_context_processors_py() -> str:
    return """\
from flask import Flask


def include(app: Flask):
    @app.context_processor
    def example__utility_processor():
        \"""
        Usage:
        {{ example__format_price(100.33) }} -> $100.33
        \"""

        def example__format_price(amount, currency='$'):
            return '{1}{0:.2f}'.format(amount, currency)

        return dict(example__format_price=example__format_price)
"""


def resources_error_handlers_py() -> str:
    return """\
from flask import Flask

from flask import render_template


def include(app: Flask):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template(
            "error.html",
            error_code=400,
            error_message="The request is invalid.",
        ), 400


    @app.errorhandler(401)
    def unauthorized(e):
        return render_template(
            "error.html",
            error_code=401,
            error_message="You are not authorized to access this page.",
        ), 401


    @app.errorhandler(403)
    def forbidden(e):
        return render_template(
            "error.html",
            error_code=403,
            error_message="You do not have permission to access this page.",
        ), 403


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template(
            "error.html",
            error_code=404,
            error_message="The page you are looking for does not exist.",

        ), 404


    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template(
            "error.html",
            error_code=405,
            error_message="The method is not allowed for the requested URL.",
        ), 405


    @app.errorhandler(410)
    def gone(e):
        return render_template(
            "error.html",
            error_code=410,
            error_message="This page is no longer available.",
        ), 410


    @app.errorhandler(429)
    def too_many_requests(e):
        return render_template(
            "error.html",
            error_code=429,
            error_message="You have made too many requests.",
        ), 429


    @app.errorhandler(500)
    def server_error(e):
        return render_template(
            "error.html",
            error_code=500,
            error_message="An internal server error has occurred.",
        ), 500

"""


def resources_filters_py() -> str:
    return """\
from flask import Flask


def include(app: Flask):
    @app.template_filter('example__num_to_month')
    def example__num_to_month(num: str) -> str:
        \"""
        Usage:
        {{ 1 | example__num_to_month }} -> January
        \"""
        if isinstance(num, int):
            num = str(num)

        months = {
            "1": "January",
            "2": "February",
            "3": "March",
            "4": "April",
            "5": "May",
            "6": "June",
            "7": "July",
            "8": "August",
            "9": "September",
            "10": "October",
            "11": "November",
            "12": "December",
        }

        if num in months:
            return months[num]
        return "Month not found"
"""


def resources_routes_py() -> str:
    return """\
from flask import Flask


def include(app: Flask):
    @app.route("/example--resources")
    def example_route():
        return "From the [app_root]/resources/routes/routes.py file"
"""


def resources_minimal_routes_py() -> str:
    return """\
from flask import Flask
from flask import render_template


def include(app: Flask):
    @app.route("/")
    def index():
        return render_template("index.html")
"""
