import typing as t
from types import ModuleType

from flask_sqlalchemy.model import DefaultMeta


class ModelRegistry:
    registry: t.Dict[str, t.Any]

    def __init__(self):
        self.registry = dict()

    def assert_exists(self, ref: str):
        if ref not in self.registry:
            raise KeyError(
                f"Model {ref} not found in model registry \n"
                f"Available models: {', '.join(self.registry.keys())}"
            )

    def get(self, ref: str) -> dict:
        self.assert_exists(ref)
        return self.registry[ref]

    def class_(self, ref: str) -> DefaultMeta:
        self.assert_exists(ref)
        return self.registry[ref]['class']

    def add(self, ref, model: t.Optional[ModuleType] = None):
        self.registry[ref] = {
            'ref': ref,
            'class': model
        }

    def __repr__(self):
        return f"ModelRegistry({self.registry})"
