"""
This module contains the security utilities for a Flask application.

Functions:

    - include_csrf: Includes a CSRF token in a GET response, and checks it during a
                    POST request.
    - checkpoint: Checks if the passed in Checkpoint passes or fails.
    - checkpoint_callable: Checks if a function you give passes.

Classes:

    - APIKeyCheckpoint: A checkpoint focused around checking the header or query param
                        for a valid token.
    - BearerCheckpoint: A checkpoint focused around working with the Bearer tokens.
    - SessionCheckpoint: A checkpoint focused around working with Flask's session.

"""

from ._include_csrf import include_csrf
from ._checkpoint_callable import checkpoint_callable
from ._checkpoint import checkpoint

from ._checkpoints import BaseCheckpoint
from ._checkpoints import APIKeyCheckpoint
from ._checkpoints import BearerCheckpoint
from ._checkpoints import SessionCheckpoint

__all__ = [
    "include_csrf",
    "checkpoint_callable",
    "checkpoint",
    # Checkpoints
    "BaseCheckpoint",
    "APIKeyCheckpoint",
    "BearerCheckpoint",
    "SessionCheckpoint",
]
