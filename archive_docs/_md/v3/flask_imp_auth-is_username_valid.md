```
Menu = flask_imp.auth/is_username_valid
Title = is_username_valid - flask_imp.auth
```

```python
from flask_imp.auth import is_username_valid
```

```python
is_username_valid(
    username: str,
    allowed: t.Optional[t.List[t.Literal["all", "dot", "dash", "under"]]] = None
) -> bool
```

---

Checks if a username is valid.

Valid usernames can only include letters,
numbers, ., -, and _ but cannot begin or end with
the last three mentioned.

##### Example "all":

```python
is_username_valid("username", allowed=["all"])
```

Output:

```text
username : WILL PASS : True
user.name : WILL PASS : True
user-name : WILL PASS : True
user_name : WILL PASS : True
_user_name : WILL PASS : False
```

##### Example "dot", "dash":

```python

is_username_valid("username", allowed=["dot", "dash"])
```

Output:

```text
username : WILL PASS : True
user.name : WILL PASS : True
user-name : WILL PASS : True
user-name.name : WILL PASS : True
user_name : WILL PASS : False
_user_name : WILL PASS : False
.user.name : WILL PASS : False
```