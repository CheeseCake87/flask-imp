```
Menu = ImpBlueprint/__init__
Title = Flask-Imp Blueprint __init__
```

```python
ImpBlueprint(dunder_name: str, config: ImpBlueprintConfig) -> None
```

---

Initializes the Flask-Imp Blueprint.

`dunder_name` should always be set to `__name__`

`config` is an instance of `ImpBlueprintConfig` that will be used to load the Blueprint's configuration. 
See [flask_imp.config / ImpBlueprintConfig](flask_imp_config-impblueprintconfig.html) for more information.
