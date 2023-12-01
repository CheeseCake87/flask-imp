from typing import Protocol, runtime_checkable, Union, Any, Optional


@runtime_checkable
class Blueprint(Protocol):
    root_path: str


@runtime_checkable
class ImpBlueprint(Protocol):
    app_path: str
    app_config: dict

    settings: dict

    def register_blueprint(self, blueprint: Blueprint):
        ...

    def _register(self, app: "Flask", options: dict) -> None:
        ...

    def _setup_imp_blueprint(self, imp_instance) -> None:
        ...


@runtime_checkable
class Flask(Protocol):
    name: str
    root_path: str
    extensions: dict
    config: dict
    static_folder: Optional[str]
    template_folder: Optional[str]

    app_context: Any

    def register_blueprint(self, blueprint: Union[Blueprint, ImpBlueprint]):
        ...
