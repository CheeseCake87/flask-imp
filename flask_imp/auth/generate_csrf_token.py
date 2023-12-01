from datetime import datetime
from hashlib import sha1


def generate_csrf_token() -> str:
    """
    Generates a SHA1 using the current date and time.

    :raw-html:`<br />`

    For use in Cross-Site Request Forgery.

    :raw-html:`<br />`

    -----

    :return: str - sha1
    """
    sha = sha1()
    sha.update(str(datetime.now()).encode("utf-8"))
    return sha.hexdigest()
