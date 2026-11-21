# hash_password

```python
from flask_imp.auth import hash_password
```

```python
hash_password(
    password: str,
    time_cost: int = 3,
    memory_cost: int = 65536,
    parallelism: int = 4,
) -> str
```

---

For use in password hashing.

To be used alongside the [flask_imp.auth / hash_password_assert](../Auth/flask_imp_auth-hash_password_assert.md) function.

Hashes the plain password using Argon2id. A random salt is generated for every hash,
and the salt, algorithm and parameters are all stored inside the returned string,
so only the one value needs to be stored in the database.

The defaults follow the RFC 9106 low-memory recommendation.

*Example:*

```python
hash_password("password")
# >>> '$argon2id$v=19$m=65536,t=3,p=4$...$...'
```

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        ...
        user = User(
            username=username,
            email=email,
            password=hash_password(request.form.get('password')),
        )
        ...
```
