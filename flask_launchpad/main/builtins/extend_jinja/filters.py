from ..functions.utilities import remove_escapes
from flask import current_app
from markupsafe import Markup


@current_app.template_filter('deco')
def decorate_code(value: str) -> str:
    return Markup(remove_escapes(value))


@current_app.template_filter('version')
def version(value: str) -> str:
    return Markup(f"{value} - {current_app.config['VERSION']}")


@current_app.template_filter('form_element')
def form_import(value: str) -> str:
    return f"macros/forms/{value}.jinja"
