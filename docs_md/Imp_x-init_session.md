```
Menu = Imp.x/init_session
Title = Imp.init_session
```

```python
init_session() -> None
```

---

Initialize the session variables found in the config. Commonly used in `app.before_request`.

```python
@app.before_request
def before_request():
    imp.init_session()
```

File: `default.config.toml`

```toml
...
[SESSION]
logged_in = false
...
```

`logged_in` is now available in the session.

```python
@app.route('/get-session-value')
def login():
    print(session['logged_in'])
    return "Check Terminal"
```

`Output: False`

Can also be used to reset the values in the session. Here's an example:

```python
@app.route('/logout')
def logout():
    session.clear()
    imp.init_session()
    return redirect(url_for('index'))
```