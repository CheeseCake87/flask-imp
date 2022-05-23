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
