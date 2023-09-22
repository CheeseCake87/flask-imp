import typing as t

from flask_sqlalchemy.model import DefaultMeta


class ModelRegistry:
    """
    A registry for SQLAlchemy models.
    This is used to store all imported SQLAlchemy models in a central location.
    Accessible via Imp.__model_registry__
    """
    registry: t.Dict[str, t.Any]

    def __init__(self):
        self.registry = dict()

    def assert_exists(self, class_name: str):
        if class_name not in self.registry:
            raise KeyError(
                f"Model {class_name} not found in model registry \n"
                f"Available models: {', '.join(self.registry.keys())}"
            )

    def add(self, ref: str, model: t.Any):
        self.registry[ref] = model

    def class_(self, class_name: str) -> DefaultMeta:
        self.assert_exists(class_name)
        return self.registry[class_name]

    def __repr__(self):
        return f"ModelRegistry({self.registry})"
