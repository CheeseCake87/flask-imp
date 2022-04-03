from ..functions.utilities import remove_escapes
from flask import current_app
from markupsafe import Markup

__all__ = ['decorate_code']


@current_app.template_filter('deco')
def decorate_code(value: str) -> str:
    return Markup(remove_escapes(value))
