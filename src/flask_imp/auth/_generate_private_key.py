import typing as t
from datetime import datetime
from hashlib import sha256, sha512
from random import randrange


def generate_private_key(
    hook: t.Optional[str] = None, algorithm: t.Literal["sha256", "sha512"] = "sha256"
) -> str:
    """
    Generates a sha256 or sha512 private key from a passed in hook value.

    If no hook is passed in, it will generate a hook using datetime.now() and a
    random number between 1 and 1000.

    :param hook: hook value to generate private key from
    :param algorithm: the algorithm sha256 | sha512 - defaults to sha256
    :return: digested sha256 | sha512
    """

    if hook is None:
        _range = randrange(1, 1000)
        hook = f"{datetime.now()}-{_range}"

    sha = sha256() if algorithm == "sha256" else sha512()
    sha.update(hook.encode("utf-8"))
    return sha.hexdigest()
