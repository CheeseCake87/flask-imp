```
Menu = flask_imp.auth/is_email_address_valid
Title = is_email_address_valid - flask_imp.auth
```

```python
from flask_imp.auth import is_email_address_valid
```

```python
is_email_address_valid(
    email_address: str
) -> bool
```

---

Checks if an email address is valid.

Is not completely RFC 5322 compliant, but it is good enough for most use cases.

Here are examples of mistakes that it will not catch:

##### Valid but fails:

```text
email@[123.123.123.123]
“email”@example.com
very.unusual.“@”.unusual.com@example.com
very.“(),:;<>[]”.VERY.“very@\\ "very”.unusual@strange.example.com
```

##### Invalid but passes:

```text
email@example.com (Joe Smith)
email@111.222.333.44444
```

##### Example:

```python
is_email_address_valid('hello@example.com')  # >>> True

is_email_address_valid('hello@hello@example.com')  # >>> False
```