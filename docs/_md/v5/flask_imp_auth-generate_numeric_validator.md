```
Menu = flask_imp.auth/generate_numeric_validator
Title = generate_numeric_validator - flask_imp.auth
```

```python
from flask_imp.auth import generate_numeric_validator
```

```python
generate_numeric_validator(length: int) -> int
```

---


Generates random choice between 1 * (length) and 9 * (length).

If the length is 4, it will generate a number between 1111 and 9999.

For use in MFA email, or unique filename generation.

##### Example:

```python
generate_numeric_validator(4)  # >>> 1234
```
