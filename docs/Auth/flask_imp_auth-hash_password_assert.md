# hash_password_assert

```python
from flask_imp.auth import hash_password_assert
```

```python
hash_password_assert(
    password: str,
    hashed_password: str,
) -> bool
```

---

For use in password checking.

To be used alongside the [flask_imp.auth / hash_password](../Auth/flask_imp_auth-hash_password.md) function.

Checks the plain password against an Argon2id hash created by `hash_password`.
The salt and parameters are read from the hash itself.

Returns `True` if the password matches, `False` if not. A malformed hash returns `False`.

*Example:*

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        ...
        user = User.query.filter_by(username=username).first()

        if user and hash_password_assert(request.form.get('password'), user.password):
            ...
```
