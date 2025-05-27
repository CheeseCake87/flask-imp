"""
This module contains the security utilities for a Flask application.

Functions:

    - api_login_check: Checks if the user is logged in for an API request using sessions.
    - include_csrf: Includes a CSRF token in a GET response, and checks it during a POST request.
    - login_check: Checks if the user is logged in using sessions.
    - permission_check: Checks if the user has the required permissions using sessions.
    - pass_function_check: Checks is a function you give passes before hitting a route.

"""

from ._include_csrf import include_csrf
from ._pass_function_check import pass_function_check
from ._checkpoint import checkpoint

__all__ = [
    "include_csrf",
    "pass_function_check",
    "checkpoint",
]
