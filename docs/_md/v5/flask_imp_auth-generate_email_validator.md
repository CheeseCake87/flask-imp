```
Menu = flask_imp.auth/generate_email_validator
Title = generate_email_validator - flask_imp.auth
```

```python
from flask_imp.auth import generate_email_validator
```

```python
generate_email_validator() -> str
```

---

Uses `generate_alphanumeric_validator` with a length of 8 to
generate a random alphanumeric value for the specific use of
validating accounts via email.

See [flask_imp.auth / generate_alphanumeric_validator](flask_imp_auth-generate_alphanumeric_validator.html) 
for more information.

##### Example:

```python
generate_email_validator()  # >>> 'A1B2C3D4'
```
