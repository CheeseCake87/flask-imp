from markupsafe import Markup
from flask import url_for


class BootstrapNavs:
    nav_items: dict

    def __init__(self, nav_items: dict):
        """
        nav_items: dict { order(int): dict { label: str, url_for: str, permission: str }
        """
        _version = "0.1"
        self.nav_items = nav_items

    def wrap_element(self, constructor: list, wrap_class: str = None) -> list:
        if wrap_class is not None:
            constructor.insert(0, f'<div class="{wrap_class}">')
            constructor.append("</div>")
        return constructor

    def tabs(self,
             wrap_class: str = None,
             endpoint: str = None,
             ):
        construction = []

        if self.nav_items is None:
            construction.append("<p>Not a valid button_action type</p>")
            return Markup("".join(construction))

        nav_items = self.nav_items
        construction.append('<ul class="nav nav-tabs">')

        for key in sorted(nav_items):
            construction.append('<li class="nav-item">')
            construction.append('<a class="nav-link')
            if endpoint is not None:
                if nav_items[key]["url_for"] == endpoint:
                    construction.append(' active')
            construction.append(
                f'" href="{url_for(nav_items[key]["url_for"])}">{nav_items[key]["label"]}</a>')
            construction.append('<li class="nav-item">')
        construction.append('</ul>')

        final = self.wrap_element(construction, wrap_class)
        return Markup("".join(final))
