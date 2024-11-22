"""
This module contains the security utilities for a Flask application.

Functions:

    - api_login_check: Checks if the user is logged in for an API request using sessions.
    - include_csrf: Includes a CSRF token in a GET response, and checks it during a POST request.
    - login_check: Checks if the user is logged in using sessions.
    - permission_check: Checks if the user has the required permissions using sessions.
    - pass_function_check: Checks is a function you give passes before hitting a route.

"""

from ._api_login_check import api_login_check
from ._include_csrf import include_csrf
from ._login_check import login_check
from ._pass_function_check import pass_function_check
from ._permission_check import permission_check

__all__ = [
    "api_login_check",
    "include_csrf",
    "login_check",
    "pass_function_check",
    "permission_check",
]
