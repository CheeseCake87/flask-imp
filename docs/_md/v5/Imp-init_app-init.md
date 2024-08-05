```
Menu = Imp/init_app, __init__
Title = Imp.init_app, __init__
```

```python
def init_app(
    app: Flask,
    config: ImpConfig
) -> None:
# -or- 
Imp(
    app: Flask,
    config: ImpConfig
)
```

---

Initializes the flask app to work with flask-imp.

See [flask_imp_config-impconfig.md](flask_imp_config-impconfig.html) for more information on the `ImpConfig` class.
