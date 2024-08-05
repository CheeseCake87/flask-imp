```
Menu = Imp/init_app, __init__
Title = Imp.init_app, __init__
```

```python
def init_app(
    app: Flask,
    config: t.Union[str, ImpConfig] = os.environ.get("IMP_CONFIG")
) -> None:
# -or- 
Imp(
    app: Flask,
    config: t.Union[str, ImpConfig] = os.environ.get("IMP_CONFIG")
)
```

---

Initializes the flask app to work with flask-imp.

If no `config` specified, an attempt to read `IMP_CONFIG` from the environment will be made.

The config value can be a toml file `my_config.toml`, for example; or an import string. An example
of an import string would be `config.Config` where `config` is the module and `Config` is the class.

If `IMP_CONFIG` is not in the environment variables, an attempt to load `config.toml` will be made. 

If `config.toml` is not found, an attempt to load a class called `Config` from `config.py` will be made. 
The Config class must be an instance of `ImpConfig` `from flask_imp import ImpConfig`.

An exception will be raised if none of the above methods are successful.
