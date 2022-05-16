from flask import current_app
from flask import session
from markupsafe import Markup

from ..functions.utilities import remove_escapes
from ..functions.memberships import get_permission_membership_from_user_id


@current_app.template_filter('deco')
def decorate_code(value: str) -> str:
    return Markup(remove_escapes(value))


@current_app.template_filter('version')
def version(value: str) -> str:
    return Markup(f"{value} - {current_app.config['VERSION']}")


@current_app.template_filter('form_element')
def form_import(value: str) -> str:
    return f"macros/forms/{value}.jinja"


@current_app.template_filter('backend_nav')
def backend_nav(blank_dict: dict) -> dict:
    blank_dict = current_app.config["BACKEND_NAV"]
    return blank_dict
