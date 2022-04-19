from .utilities import get_app_root
from .utilities import is_dir
from .utilities import is_file


class StructureBuilder:
    def __init__(self, structure_name: str = "fl_default"):
        self.app_root = get_app_root()
        self.structure_name = structure_name

    def extend(self, extending: str) -> str:
        """
        Looks for the template to extend in the specified structure. If the template to extend is not found, it will
        look for the template to extend in the default structure. If again not found, it will return an error page.
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

        return "structures/fl_default/error_pages/template_extend_error.html"

    def include(self, including: str) -> str:
        """
        Looks for the file to be included in the page. If the file is not found on the custom structure, it will
        look in the default structure. If it cannot file the file at all, it will return an error include file.
        :param including:
        :return:
        """
        _structure = f"{self.app_root}/builtins/templates/structures/{self.structure_name}/includes"
        _default_structure = f"{self.app_root}/builtins/templates/structures/fl_default/includes"
        if is_dir(_structure):
            if is_file(f"{_structure}/{including}"):
                return f"structures/{self.structure_name}/includes/{including}"

            if is_file(f"{_default_structure}/{including}"):
                return f"structures/fl_default/includes/{including}"

        return "structures/fl_default/error_pages/template_include_error.html"

    def error(self, error_page: str) -> str:
        """
        Looks for the error page to render in the specified structure. If the error page is not found, it will
        look for the error page to render in the default structure. If again not found, it will return an error page.
        :param extending:
        :return:
        """
        _structure = f"{self.app_root}/builtins/templates/structures/{self.structure_name}/error_pages"
        _default_structure = f"{self.app_root}/builtins/templates/structures/fl_default/error_pages"
        if is_dir(_structure):
            if is_file(f"{_structure}/{error_page}"):
                return f"structures/{self.structure_name}/error_pages/{error_page}"

            if is_file(f"{_default_structure}/{error_page}"):
                return f"structures/fl_default/error_pages/{error_page}"

        return "structures/fl_default/error_pages/template_extend_error.html"

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
