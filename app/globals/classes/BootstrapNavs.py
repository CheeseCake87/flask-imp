from markupsafe import Markup
from flask import url_for


class BootstrapNavs:
    _all: dict = {}
    _endpoint: str = ""

    def __init__(self, endpoint: str = "") -> None:
        self._endpoint = endpoint
        self.clear()

    def all(self) -> dict:
        if self._all == {}:
            return {"": ""}
        return self._all

    def add(self, element: object) -> None:
        tack = {
            len(self._all): element
        }
        self._all.update(tack)

    def remove(self, name) -> None:
        self._all.pop(name)

    def update(self, name, element) -> None:
        self._all[name] = element

    def clear(self) -> None:
        self._all.clear()

    def no_space(self, string: str) -> str:
        return string.replace(" ", "").lower()

    def title(self, string: str) -> str:
        return string.title()

    def wrap_element(self, constructor: list, wrap_class: str = None) -> list:
        if wrap_class is not None:
            constructor.insert(0, f'<div class="{wrap_class}">')
            constructor.append("</div>")
        return constructor

    def tabs(self) -> dict:
        tabs_dict = {}
        tabs_dict.clear()
        tabs_dict["start_of_tabs"] = Markup('<ul class="nav nav-tabs">')
        tabs_dict.update(self.all())
        tabs_dict["end_of_tabs"] = Markup('</ul>')
        return tabs_dict

    def tab(self,
            label: str,
            tab_class: str = "",
            endpoint: str = None,
            match_endpoint: bool = True,
            override_url: str = "",
            active: bool = False,
            disabled: bool = False,
            wrap_class: str = None,
            ):

        construction = ['<li class="nav-item">', '<a class="nav-link']

        if tab_class != "":
            construction.append(f' {tab_class}')
        if active:
            construction.append(' active')
        if disabled:
            construction.append(' disabled')

        else:
            if match_endpoint:
                if endpoint == self._endpoint:
                    construction.append(' active')

        construction.append('"')

        if override_url != "":
            construction.append(f' href="{override_url}">{label}</a>')
            construction.append('</li>')
            final = self.wrap_element(construction, wrap_class)
            return Markup("".join(final))

        if endpoint is not None:
            construction.append(f' href="{url_for(endpoint)}">{label}</a>')
            construction.append('</li>')
            final = self.wrap_element(construction, wrap_class)
            return Markup("".join(final))

        construction.append(f' href="#">{label}</a>')
        construction.append('</li>')
        final = self.wrap_element(construction, wrap_class)
        return Markup("".join(final))
