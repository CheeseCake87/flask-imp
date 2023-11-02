```
Menu = flask_imp.auth/encrypt_password
Title = encrypt_password - flask_imp.auth
```

```python
from flask_imp.auth import encrypt_password
```

```python
encrypt_password(
    password: str,
    salt: str,
    encryption_level: int = 512,
    pepper_length: int = 1,
    pepper_position: t.Literal["start", "end"] = "end"
) -> str
```

---

For use in password hashing.

To be used alongside the [flask_imp.auth / authenticate_password](flask_imp_auth-authenticate_password.html) function.

Takes the plain password, applies a pepper, salts it, then produces a digested sha512 or sha256 if specified.

Can set the encryption level to 256 or 512, defaults to 512.

Can set the pepper length, defaults to 1. Max is 3.

Can set the pepper position, "start" or "end", defaults to "end".

**Note:**

- You must inform the authenticate_password function of the pepper length used to hash the password.
- You must inform the authenticate_password function of the position of the pepper used to hash the password.
- You must inform the authenticate_password function of the encryption level used to hash the password.

#### Encryption Scenario:

```
Plain password: "password"
Generated salt: "^%$*" (randomly generated)
Generated pepper (length 1): "A" (randomly generated)
Pepper position: "end"
```

1. Pepper is added to the end of the plain password: "passwordA"
2. Salt is added to the end of the peppered password: "passwordA^%$*"
3. Password is hashed: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0..."
4. Salt and hashed password are then stored in the database.

