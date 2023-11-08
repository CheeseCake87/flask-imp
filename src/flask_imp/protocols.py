from typing import Protocol, runtime_checkable


@runtime_checkable
class Blueprint(Protocol):
    root_path: str


@runtime_checkable
class Flask(Protocol):
    name: str
    root_path: str
    extensions: dict
    config: dict

    def app_context(self):
        ...

    def register_blueprint(self, blueprint: Blueprint):
        ...
