import multiprocessing
import typing as t
from itertools import product
from string import ascii_letters

from more_itertools import batched

from ._private_funcs import _guess_block


def authenticate_password(
    input_password: str,
    database_password: str,
    database_salt: str,
    encryption_level: int = 512,
    pepper_length: int = 1,
    pepper_position: t.Literal["start", "end"] = "end",
    use_multiprocessing: bool = False,
) -> bool:
    """
    Takes the plain input password, the stored hashed password along with the stored salt
    and will try every possible combination of pepper values to find a match.

    *Note:* use_multiprocessing is not compatible with coroutine workers, e.g. eventlet/gevent
    commonly used with socketio.

    **You must know:**

    - the length of the pepper used to hash the password.
    - the position of the pepper used to hash the password.
    - the encryption level used to hash the password.

    :param input_password: plain password
    :param database_password: hashed password from database
    :param database_salt: salt from database
    :param encryption_level: encryption used to generate database password
    :param pepper_length: length of pepper used to generate database password
    :param pepper_position: "start" or "end" - position of pepper used to generate database password
    :param use_multiprocessing: use multiprocessing to speed up the process (not compatible with eventlet/gevent)
    :return: True if match, False if not
    """

    if pepper_length > 3:
        pepper_length = 3

    _guesses = {"".join(i) for i in product(ascii_letters, repeat=pepper_length)}

    if not use_multiprocessing:
        for guess in _guesses:
            if _guess_block(
                {guess},
                input_password,
                database_password,
                database_salt,
                encryption_level,
                pepper_position,
            ):
                return True

        return False

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
