import re


def is_email_address_valid(email_address: str) -> bool:
    """
    Checks if email_address is a valid email address.

    Is not completely RFC 5322 compliant, but it is good enough for most use cases.

    :raw-html:`<br />`

    Here are examples of mistakes that it will not catch:

    :raw-html:`<br />`

    Valid but fails:

     - email@[123.123.123.123] is VALID => PASSED : False
     - “email”@example.com is VALID => PASSED : False
     - very.unusual.“@”.unusual.com@example.com is VALID => PASSED : False
     - very.“(),:;<>[]”.VERY.“very@\\ "very”.unusual@strange.example.com is VALID => PASSED : False

     Invalid but passes:

     - email@example.com (Joe Smith) is INVALID => PASSED : True
     - email@111.222.333.44444 is INVALID => PASSED : True


    :raw-html:`<br />`

    -----

    :param email_address: str
    :return: bool
    """
    pattern = re.compile(
        r"[a-z\d!#$%&'*+?^_`{|}~-]+(?:\.[a-z\d!#$%&'*+?^_`"
        r"{|}~-]+)*@(?:[a-z\d](?:[a-z\d-]*[a-z\d])?\.)+[a-z\d](?:[a-z\d-]*[a-z\d])?",
        re.IGNORECASE,
    )
    return bool(pattern.match(email_address))
