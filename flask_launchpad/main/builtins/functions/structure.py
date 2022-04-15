from .utilities import get_app_root
from .utilities import is_dir
from .utilities import is_file


class StructureBuilder:
    def __init__(self, structure_name: str):
        self.app_root = get_app_root()
        self.structure_name = structure_name

    def extend(self, extending: str) -> str:
        """

        :param extending:
        :return:
        """
        _structure = f"{self.app_root}/builtins/templates/structures/{self.structure_name}/extends"
        _default_structure = f"{self.app_root}/builtins/templates/structures/fl_default/extends"
        if is_dir(_structure):
            if is_file(f"{_structure}/{extending}"):
                return f"structures/{self.structure_name}/extends/{extending}"

            if is_file(f"{_default_structure}/{extending}"):
                return f"structures/fl_default/extends/{extending}"

        return f"system/error.html"

    def include(self, including: str) -> str:
        """

        :param extending:
        :return:
        """
        _structure = f"{self.app_root}/builtins/templates/structures/{self.structure_name}/includes"
        _default_structure = f"{self.app_root}/builtins/templates/structures/fl_default/includes"
        if is_dir(_structure):
            if is_file(f"{_structure}/{including}"):
                return f"structures/{self.structure_name}/includes/{including}"

            if is_file(f"{_default_structure}/{including}"):
                return f"structures/fl_default/includes/{including}"

        return f"system/error.html"

    def name(self) -> str:
        """
        Simply returns the name of the structure, but checks the folder exists first. If it does not
        it will default to fl_default
        :return:
        """
        _location = f"{self.app_root}/builtins/templates/structures/{self.structure_name}"
        if is_dir(_location):
            return self.structure_name
        return "fl_default"
