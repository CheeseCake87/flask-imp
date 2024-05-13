```
Menu = flask_imp.auth/authenticate_password
Title = authenticate_password - flask_imp.auth
```

```python
from flask_imp.auth import authenticate_password
```

```python
authenticate_password(
    input_password: str,
    database_password: str,
    database_salt: str,
    encryption_level: int = 512,
    pepper_length: int = 1,
    pepper_position: t.Literal["start", "end"] = "end",
    use_multiprocessing: bool = False
) -> bool
```

---

For use in password hashing.

To be used alongside the [flask_imp.auth / encrypt_password](flask_imp_auth-encrypt_password.html) function.

Takes the plain input password, the stored hashed password along with the stored salt
and will try every possible combination of pepper values to find a match.

**Note:**

**use_multiprocessing is not compatible with coroutine workers, e.g. eventlet/gevent
commonly used with socketio.**

If you are using socketio, you must set use_multiprocessing to False (default).

**Note:**

- You must know the pepper length used to hash the password.
- You must know the position of the pepper used to hash the password.
- You must know the encryption level used to hash the password.

#### Authentication Scenario:

```
Plain password: "password"
Generated salt: "^%$*" (randomly generated)
Generated pepper (length 1): "A" (randomly generated)
Pepper position: "end"
```

```python
input_password = "password"
database_password = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0..." # pulled from database
database_salt = "^%$*" # pulled from database

authenticate_password(
    input_password,
    database_password,
    database_salt
)  # >>> True
```
