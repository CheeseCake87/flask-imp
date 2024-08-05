```
Menu = Imp.x/model
Title = Imp.model
```

```python
model(class_: str) -> DefaultMeta
```

---

Returns the SQLAlchemy model class for the given class name that was imported using `Imp.import_models` or 
`Blueprint.import_models`.

This method has convenience for being able to omit the need to import the model class from the file it was defined in.
However, it is not compatible with IDE type hinting.

For example:

```python
from app.models.boats import Boats
from app.models.cars import Cars
```

Can be replaced with:

```python
from app import imp

Boats = imp.model("Boats")
Cars = imp.model("Cars")
```

Or used directly:

```python
from app import imp

all_boats = imp.model("Boats").select_all()
```


file: `models/boats.py`

```python
from app import db


class Boats(db.Model):
    name = db.Column(db.String())

    @classmethod
    def select_all(cls):
        return db.session.execute(
            db.select(cls)
        ).scalars().all()
```
