```
Menu = flask_imp.auth/generate_password
Title = generate_password - flask_imp.auth
```

```python
from flask_imp.auth import generate_password
```

```python
generate_password(style: str = "mixed", length: int = 3) -> str
```

---

Generates a password of (length) characters.

The Default length is 3.

Style options: "animals", "colors", "mixed" - defaults to "mixed"

##### Example:

```python
generate_password(style="animals", length=3)  # >>> 'Cat-Goat-Pig12'
```
