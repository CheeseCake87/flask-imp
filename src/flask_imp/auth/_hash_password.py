from argon2 import PasswordHasher


def hash_password(
    password: str,
    time_cost: int = 3,
    memory_cost: int = 65536,
    parallelism: int = 4,
) -> str:
    """
    Hashes a plain password using Argon2id.

    A random salt is generated for every hash and stored inside the returned
    string, along with the algorithm and parameters used. There is no need
    to store the salt separately.

    The defaults follow the RFC 9106 low-memory recommendation.

    To be used alongside the hash_password_assert function.

    :param password: str - plain password
    :param time_cost: int - number of iterations - defaults to 3
    :param memory_cost: int - memory usage in kibibytes - defaults to 65536 (64 MiB)
    :param parallelism: int - number of parallel threads - defaults to 4
    :return str: the encoded Argon2id hash, e.g. "$argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>"
    """
    return PasswordHasher(
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
    ).hash(password)
