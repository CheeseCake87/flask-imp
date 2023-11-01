```
Menu = flask_imp.auth/generate_private_key
Title = generate_private_key - flask_imp.auth
```

```python
from flask_imp.auth import generate_private_key
```

```python
generate_private_key(hook: t.Optional[str]) -> str
```

---

Generates a sha256 private key from a passed in hook value.

If no hook is passed in, it will generate a hook using datetime.now() and a
random number between 1 and 1000.

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        ...
        salt = generate_salt()
        password = request.form.get('password')
        encrypted_password = encrypt_password(password, salt)
        ...
        user = User(
            username=username,
            email=email,
            password=encrypted_password,
            salt=salt,
            private_key=generate_private_key(hook=username)
        )
        ...
```
