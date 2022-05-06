from flask import current_app

from ..functions.utilities import get_app_root
from ..functions.utilities import is_dir
from ..functions.utilities import is_file

default_app_config_structure = current_app.config["STRUCTURE"]


class StructureBuilder:
    def __init__(self, structure_name: str):
        if structure_name == "~":
            self._structure_name = default_app_config_structure
        else:
            self._structure_name = structure_name

        self._app_root = get_app_root()
        self._default_structure_name = default_app_config_structure
        self._structure = f"{self._app_root}/structures/{self._structure_name}"
        self._default_structure = f"{self._app_root}/structures/fl_default"

    def extend(self, extending: str) -> str:
        """
        Looks for the template to extend in the specified structure. If the template to extend is not found, it will
        look for the template to extend in the default structure. If again not found, it will return an error page.
        :param extending:
        :return:
        """
        if is_dir(self._structure):
            if is_file(f"{self._structure}/extends/{extending}"):
                return f"{self._structure_name}/extends/{extending}"

            if is_file(f"{self._default_structure}/extends/{extending}"):
                return f"{self._default_structure_name}/extends/{extending}"

        return f"{self._default_structure}/error_pages/template_extend_error.html"

    def include(self, including: str) -> str:
        """
        Looks for the file to be included in the page. If the file is not found on the custom structure, it will
        look in the default structure. If it cannot file the file at all, it will return an error include file.
        :param including:
        :return:
        """
        if is_dir(self._structure):
            if is_file(f"{self._structure}/includes/{including}"):
                return f"{self._structure_name}/includes/{including}"

            if is_file(f"{self._default_structure}/includes/{including}"):
                return f"{self._default_structure_name}/includes/{including}"

        return f"{self._default_structure}/error_pages/template_include_error.html"

    def error(self, error_page: str) -> str:
        """
        Looks for the error page to render in the specified structure. If the error page is not found, it will
        look for the error page to render in the default structure. If again not found, it will return an error page.
        :param error_page:
        :return:
        """
        if is_dir(self._structure):

            if is_file(f"{self._structure}/error_pages/{error_page}"):
                return f"{self._structure_name}/error_pages/{error_page}"

            if is_file(f"{self._default_structure}/error_pages/{error_page}"):
                return f"{self._default_structure_name}/error_pages/{error_page}"

        return f"{self._default_structure_name}/error_pages/template_extend_error.html"

    def render(self, render_page: str) -> str:
        """
        Looks for a full render page in each module folder, if not found it renders the error page.
        :param render_page:
        :return:
        """
        if is_dir(self._structure):
            if is_file(f"{self._structure}/renders/{render_page}"):
                return f"{self._structure_name}/renders/{render_page}"

            if is_file(f"{self._default_structure}/renders/{render_page}"):
                return f"{self._default_structure_name}/renders/{render_page}"

        return f"{self._default_structure}/error_pages/template_render_error.html"

    def name(self) -> str:
        """
        Simply returns the name of the structure, but checks the folder exists first. If it does not
        it will default to fl_default
        :return:
        """
        if is_dir(self._structure):
            return self._structure_name
        return "fl_default"
