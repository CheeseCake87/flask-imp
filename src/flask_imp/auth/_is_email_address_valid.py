import re


def is_email_address_valid(email_address: str) -> bool:
    """
    Checks if email_address is a valid email address.

    Is not completely RFC 5322 compliant, but it is good enough for most use cases.

    Here are examples of mistakes that it will not catch::

        VALID but fails:
        - email@[123.123.123.123]
        - “email”@example.com
        - very.unusual.“@”.unusual.com@example.com
        - very.“(),:;<>[]”.VERY.“very@\\ "very”.unusual@strange.example.com

         INVALID but passes:
         - email@example.com (Joe Smith)
         - email@111.222.333.44444

    -----

    :param email_address: email address to validate
    :return: True if email_address is valid, False otherwise
    """
    pattern = re.compile(
        r"[a-z\d!#$%&'*+?^_`{|}~-]+(?:\.[a-z\d!#$%&'*+?^_`"
        r"{|}~-]+)*@(?:[a-z\d](?:[a-z\d-]*[a-z\d])?\.)+[a-z\d](?:[a-z\d-]*[a-z\d])?",
        re.IGNORECASE,
    )
    return bool(pattern.match(email_address))
