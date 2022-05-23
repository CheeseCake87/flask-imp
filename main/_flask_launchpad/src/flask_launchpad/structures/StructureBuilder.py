from os import path
from markupsafe import Markup
from flask import current_app


class StructureBuilder:
    structure_name = None
    structure_path = None

    def __init__(self, structure_name: str = None):
        self.structure_name = structure_name

    def init_app(self) -> None:
        if self.structure_name is None:
            raise ImportError("Structure name has not been passed in.")

        if not current_app.config["structure_folders"]:
            raise ImportError(
                "No structure folders have been registered. In the app init add: fl.register_structure_folder('name')")

        for key, value in current_app.config["structure_folders"].items():
            if path.isdir(f"{value}/{self.structure_name}"):
                self.structure_path = f"{value}/{self.structure_name}"
                return

    def extend(self, extending: str) -> str:
        """
        Looks for the template to extend in the specified structure.
        """

        if path.isfile(f"{self.structure_path}/extends/{extending}"):
            return f"{self.structure_name}/extends/{extending}"

        return Markup(f"Extend template error, unable to find: {extending}")

    def include(self, including: str) -> str:
        """
        Looks for the file to be included in the page.
        """
        if path.isfile(f"{self.structure_path}/includes/{including}"):
            return f"{self.structure_name}/includes/{including}"

        return Markup(f"Include template error, unable to find: {including}")

    def error(self, error_page: str) -> str:
        """
        Looks for the error page to render in the specified structure.
        """
        if path.isfile(f"{self.structure_path}/error_pages/{error_page}"):
            return f"{self.structure_name}/error_pages/{error_page}"

        return Markup(f"Error page render error, unable to find: {error_page}")

    def render(self, render_page: str) -> str:
        """
        Looks for a full render page in each module folder, if not found it renders the error page.
        """
        if path.isfile(f"{self.structure_path}/renders/{render_page}"):
            return f"{self.structure_name}/renders/{render_page}"

        return Markup(f"Page render error, unable to find: {render_page}")

    def name(self) -> str:
        """
        Simply returns the name of the structure
        """
        return self.structure_name
