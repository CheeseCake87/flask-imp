import typing as t
from datetime import datetime
from hashlib import sha256
from random import randrange


def generate_private_key(hook: t.Optional[str]) -> str:
    """
    Generates a sha256 private key from a passed in hook value.

    If no hook is passed in, it will generate a hook using datetime.now() and a
    random number between 1 and 1000.

    :param hook: hook value to generate private key from
    :return: digested sha256
    """

    if hook is None:
        _range = randrange(1, 1000)
        hook = f"{datetime.now()}-{_range}"

    sha = sha256()
    sha.update(hook.encode("utf-8"))
    return sha.hexdigest()
