import secrets
from datetime import datetime
from hashlib import sha1


def generate_csrf_token() -> str:
    """
    Generates a SHA1 using the current date and time combined with
    cryptographically secure random bytes.

    For use in Cross-Site Request Forgery.

    :return: sha1 hash of the current date and time plus random entropy
    """
    sha = sha1()
    sha.update(f"{datetime.now()}{secrets.token_hex(16)}".encode("utf-8"))
    return sha.hexdigest()
