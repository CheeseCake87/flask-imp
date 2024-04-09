import importlib
import typing as t

from flask_imp import ImpConfig, ImpBlueprintConfig


def raise_error(config: str) -> None:
    raise ValueError(
        f"\n"
        f"{config} is not an instance of "
        f"ImpConfig or ImpBlueprintConfig"
        f"\n"
        f"Remember to inherit from ImpConfig or ImpBlueprintConfig "
        f"\n"
        f"from flask_imp import ImpConfig, ImpBlueprintConfig"
        f"\n"
        f"class Config(ImpConfig): ..."
    )


def load_object(config: str) -> t.Union[ImpConfig, ImpBlueprintConfig]:
    import_split = config.split(".")

    config_module = importlib.import_module(".".join(import_split[:-1]))

    try:
        config = getattr(config_module, import_split[-1])()

        if isinstance(config, ImpConfig) or isinstance(config, ImpBlueprintConfig):
            return config

    except AttributeError:
        raise_error(config)

    raise_error(config)
