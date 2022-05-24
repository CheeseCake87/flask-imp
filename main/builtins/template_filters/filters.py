from flask import current_app
from markupsafe import Markup


@current_app.template_filter('deco')
def decorate_code(value: str) -> str:
    return Markup(value)
