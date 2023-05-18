import typing as t
from types import ModuleType

from flask_sqlalchemy.model import DefaultMeta


class ModelRegistry:
    registry: t.Dict[str, t.Any]

    def __init__(self):
        self.registry = dict()

    def assert_exists(self, class_name: str):
        if class_name not in self.registry:
            raise KeyError(
                f"Model {class_name} not found in model registry \n"
                f"Available models: {', '.join(self.registry.keys())}"
            )

    def add(self, ref, model: t.Optional[ModuleType] = None):
        self.registry[ref] = model

    def class_(self, class_name: str) -> DefaultMeta:
        self.assert_exists(class_name)
        return self.registry[class_name]

    def __repr__(self):
        return f"ModelRegistry({self.registry})"
