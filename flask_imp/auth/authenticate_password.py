import multiprocessing
import typing as t
from itertools import product
from string import ascii_letters

from more_itertools import batched

from .__private_funcs__ import _guess_block


def authenticate_password(
    input_password: str,
    database_password: str,
    database_salt: str,
    encryption_level: int = 512,
    pepper_length: int = 1,
    pepper_position: t.Literal["start", "end"] = "end",
) -> bool:
    """
    Takes the plain input password, the stored hashed password along with the stored salt
    and will try every possible combination of pepper values to find a match.

    :raw-html:`<br />`

    .. Note::

        You must know the length of the pepper used to hash the password.

        You must know the position of the pepper used to hash the password.

        You must know the encryption level used to hash the password.

    :raw-html:`<br />`

    -----

    :param input_password: str - plain password
    :param database_password: str - hashed password from database
    :param database_salt: str - salt from database
    :param encryption_level: int - encryption used to generate database password
    :param pepper_length: int - length of pepper used to generate database password
    :param pepper_position: str - "start" or "end" - position of pepper used to generate database password
    :return: bool - True if match, False if not
    """

    if pepper_length > 3:
        pepper_length = 3

    _guesses = {"".join(i) for i in product(ascii_letters, repeat=pepper_length)}

    thread_pool = multiprocessing.Pool(processes=pepper_length)
    threads = []

    for batch in batched(_guesses, 1000):
        threads.append(
            thread_pool.apply_async(
                _guess_block,
                args=(
                    batch,
                    input_password,
                    database_password,
                    database_salt,
                    encryption_level,
                    pepper_position,
                ),
            )
        )

    for thread in threads:
        if thread.get():
            return True

    return False
