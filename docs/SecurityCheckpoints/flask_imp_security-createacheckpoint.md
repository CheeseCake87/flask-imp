# Create a Checkpoint

You can create your own checkpoint by inheriting from the `BaseCheckpoint` class:

```python
from flask_imp.security import BaseCheckpoint
```

```python
class MyCheckpoint(BaseCheckpoint):
    my_attrs_here: str

    def __init__(self, passed_in_arg: str):
        self.my_attrs_here = passed_in_arg

    def pass_(self) -> <truly>:
        # conditional check here, must return truly.
        ...
```

```python
MyCheckpoint(
    passed_in_arg: str,
).action(
    pass_url: t.Optional[t.Union[str | partial]] = None,
    fail_url: t.Optional[t.Union[str | partial]] = None,
    fail_json: t.Optional[t.Dict[str, t.Any]] = None,
    fail_status: int = 403,
    message: t.Optional[str] = None,
    message_category: str = "message"
)
```
