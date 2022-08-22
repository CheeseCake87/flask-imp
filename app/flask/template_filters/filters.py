from flask import current_app
from markupsafe import Markup


@current_app.template_filter('example')
def decorate_code(value: str) -> str:
    return Markup(f"The string value passed in is: {value} -> here is something after that value.")
