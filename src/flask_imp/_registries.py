from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from flask_sqlalchemy.model import DefaultMeta


class ModelRegistry:
    """
    A registry for SQLAlchemy models.
    This is used to store all imported SQLAlchemy models in a central location.
    Accessible via Imp.__model_registry__
    """

    registry: t.Dict[str, t.Any]

    def __init__(self) -> None:
        self.registry = {}

    def assert_exists(self, class_name: str) -> None:
        """
        Assert that the model exists in the registry.

        :param class_name: the name of the model to check for
        """
        if class_name not in self.registry:
            raise KeyError(
                f"Model {class_name} not found in model registry \n"
                f"Available models: {', '.join(self.registry.keys())}"
            )

    def add(self, ref: str, model: t.Any) -> None:
        """
        Add a model to the registry.

        :param ref: the name of the model
        :param model: the model to add
        """
        self.registry[ref] = model

    def class_(self, class_name: str) -> t.Union[DefaultMeta, t.Any]:
        """
        Get a model from the registry.

        :param class_name: the name of the model to get
        :return: the model
        """
        self.assert_exists(class_name)
        return self.registry[class_name]

    @property
    def instance(self) -> "ModelRegistry":
        """
        Return the instance of the ModelRegistry.

        :return: the instance of the ModelRegistry
        """
        return self

    def __repr__(self) -> str:
        return f"ModelRegistry({self.registry})"
