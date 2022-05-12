from markupsafe import Markup


class BootstrapForms:
    _all = {}

    def __init__(self):
        _version = "0.1"
        self.clear()

    def all(self) -> dict:
        if self._all == {}:
            return {"": ""}
        return self._all

    def add(self, name: str, element: Markup = None, element_list: list = None) -> None:
        null_marker = ":null:"
        if element is not None:
            if null_marker in element:
                element = element.replace(null_marker, name)
            tack = {name: element}
            self._all.update(tack)
            return

        if element_list is not None:
            unpack_list = []
            for index, element in enumerate(element_list):
                if null_marker in element:
                    unpack_list.append(element.replace(null_marker, f"{name}_{index}"))
                else:
                    unpack_list.append(element)
            tack = {name: unpack_list}
            self._all.update(tack)
            return

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

    def wrap_element(self, constructor: list, wrap_class: str = None, wrap_inner_class: str = None) -> list:
        if wrap_inner_class is not None:
            constructor.insert(0, f'<div class="{wrap_inner_class}">')
            constructor.append("</div>")
        if wrap_class is not None:
            constructor.insert(0, f'<div class="{wrap_class}">')
            constructor.append("</div>")
        return constructor

    def apply_input_group(self, constructor) -> list:
        constructor.insert(0, '<div class="input-group">')
        constructor.append('</div>')
        return constructor

    def prepend_label_func(self, constructor: list, label: str) -> list:
        if '<div class="input-group">' not in constructor:
            constructor = self.apply_input_group(constructor)
        constructor.insert(1, f'</div>')
        constructor.insert(1,
                           f'<span class="input-group-text" id="inputGroup-sizing-default">{label}</span>')
        constructor.insert(1, f'<div class="input-group-prepend">')
        return constructor

    def append_label_func(self, constructor: list, label: str) -> list:
        if '<div class="input-group">' not in constructor:
            constructor = self.apply_input_group(constructor)
        constructor.append(f'<div class="input-group-append">')
        constructor.append(
            f'<span class="input-group-text" id="inputGroup-sizing-default">{label}</span>')
        constructor.append(f'</div>')
        return constructor

    def prepend_button_func(self, constructor: list, button_object: str) -> list:
        if '<div class="input-group">' not in constructor:
            constructor = self.apply_input_group(constructor)
        constructor.insert(1, f'</div>')
        constructor.insert(1, button_object)
        constructor.insert(1, f'<div class="input-group-prepend">')
        constructor.insert(1, f'<div class="input-group">')
        constructor.append('</div>')
        return constructor

    def append_button_func(self, constructor: list, button_object: str) -> list:
        if '<div class="input-group">' not in constructor:
            constructor.append(f'<div class="input-group-append">')
            constructor.append(button_object)
            constructor.append(f'</div>')
            constructor = self.apply_input_group(constructor)
            return constructor

        constructor.insert(constructor.__len__() - 2, f'<div class="input-group-append">')
        constructor.insert(constructor.__len__() - 2, button_object)
        constructor.append(f'</div>')
        return constructor

    def hidden(self,
               name: str = ":null:",
               value: str = "submit"
               ):
        return Markup(
            f'<input type="hidden" name="{self.no_space(name)}" id="{self.no_space(name)}" value="{value}" />')

    def switch(self,
               name: str = ":null:",
               label: str = "",
               input_class: str = "",
               onclick: str = "",
               wrap_class: str = None,
               wrap_inner_class: str = None,
               checked: bool = False,
               disabled: bool = False,
               required: bool = False,
               ) -> Markup:

        construction = ['<div class="form-check form-switch">', '<input class="form-check-input']
        if input_class != "":
            construction.append(f'{input_class}')
        construction.append(f'" type="checkbox" name="{name}" id="{name}"')
        if onclick != "":
            construction.append(f' onclick="{onclick}"')
        if checked:
            construction.append(' checked')
        if disabled:
            construction.append(' disabled')
        if required:
            construction.append(' required')
        construction.append('>')
        if label != "":
            construction.append(
                f'<label class="form-check-label" for="{name}">{label}</label>'
            )
        construction.append('</div>')
        final = self.wrap_element(construction, wrap_class, wrap_inner_class)
        return Markup("".join(final))

    def button(self,
               label: str,
               element_type: str = "button",
               button_action: str = "button",
               button_class: str = None,
               href: str = "#",
               target: str = "",
               wrap_class: str = None,
               wrap_inner_class: str = None,
               disabled: bool = False,
               ) -> Markup:
        """
        Generates a Bootstrap button.
        element_type: button , a
        button_action: button , submit , rest
        Default element_type: button
        """

        construction = []
        valid_button_action = ["button", "submit", "reset"]
        if button_class is not None:
            if "btn " not in button_class:
                button_class = "btn " + button_class
        else:
            button_class = "btn"

        if element_type == "a":
            construction.append(f'<a href="{href}" ')
            construction.append(f'class="{button_class}')
            if target != "":
                construction.append(f'target="{target}')
            if disabled:
                construction.append(' disabled')
            construction.append(f'" role="button">{label}</a>')
            final = self.wrap_element(construction, wrap_class)
            return Markup("".join(final))

        if element_type == "button":
            if button_action not in valid_button_action:
                construction.append("<p>Not a valid button_action type</p>")
                return Markup("".join(construction))
            construction.append(f'<button type="{button_action}" ')
            construction.append(f'class="{button_class}" ')
            if disabled:
                construction.append('disabled')
            construction.append(f'>{label}</button>')
            final = self.wrap_element(construction, wrap_class, wrap_inner_class)
            return Markup("".join(final))

        construction.append("<p>Not a valid element type</p>")
        return Markup("".join(construction))

    def input(self,
              name: str = ":null:",
              label: str = "",
              prepend_label: str = "",
              append_label: str = "",
              prepend_button: str = "",
              append_button: str = "",
              placeholder: str = "",
              input_type: str = "text",
              input_class: str = "",
              input_id: str = "",
              wrap_class: str = None,
              wrap_inner_class: str = None,
              required: bool = False,
              readonly: bool = False,
              disabled: bool = False,
              multiple: bool = False,
              autofocus: bool = False,
              value: str = None,
              ) -> Markup:

        _name = self.no_space(name)
        _label = self.title(label)

        construction = [
            f'<input ',
            f'type="{input_type}" ',
            f'name="{_name}" ',
            'class="form-control',
        ]

        if input_class != "":
            construction.append(f' {input_class}')

        construction.append(f'" id="{_name}', )
        if input_id != "":
            construction.append(f' {input_id}')
        construction.append(f'"')

        if value:
            construction.append(f'value="{value}" ')

        if placeholder != "":
            construction.append(f'placeholder="{placeholder}" ')

        if required:
            construction.append('required ')

        if readonly:
            construction.append('readonly ')

        if disabled:
            construction.append('disabled ')

        if multiple:
            construction.append('multiple ')

        if autofocus:
            construction.append('autofocus ')

        construction.append("/>")

        if prepend_label != "" and prepend_button != "":
            return Markup("<p>Not able to prepend both a label and a button</p>")

        if append_label != "" and append_button != "":
            return Markup("<p>Not able to append both a label and a button</p>")

        if prepend_label != "":
            construction = self.prepend_label_func(construction, prepend_label)

        if append_label != "":
            construction = self.append_label_func(construction, prepend_label)

        if prepend_button != "":
            construction = self.prepend_button_func(construction, prepend_button)

        if append_button != "":
            construction = self.append_button_func(construction, append_button)

        if label != "":
            construction.insert(0, f'<label for="{_name}" class="mb-2">{_label}</label>')

        final = self.wrap_element(construction, wrap_class, wrap_inner_class)
        return Markup("".join(final))

    def select(self,
               name: str = ":null:",
               label: str = "",
               prepend_label: str = "",
               append_label: str = "",
               prepend_button: str = "",
               append_button: str = "",
               input_class: str = "",
               wrap_class: str = None,
               wrap_inner_class: str = None,
               selected: str = "",
               values_list: list = None,
               values_dict: dict = None,
               values_group_dict: dict = None,
               required: bool = False,
               readonly: bool = False,
               disabled: bool = False,
               multiple: bool = False,
               ):

        _name = self.no_space(name)
        _label = self.title(label)

        construction = [
            '<select ',
            f'name="{_name}" ',
            f'id="{_name}" ',
            'style="-webkit-appearance: menulist;" ',
            f'class="form-control form-override {input_class}" ',
        ]

        if required:
            construction.append(" required")

        if readonly:
            construction.append(" readonly")

        if disabled:
            construction.append(" disabled")

        if multiple:
            construction.append(" multiple")

        construction.append(">")

        if values_list:
            for value in values_list:
                construction.append(f'<option value="{value}">{value}</option>')

        if values_dict:
            for key, value in values_dict.items():
                construction.append(f'<option value="{value}">{key}</option>')

        if values_group_dict:
            for group, group_dict in values_group_dict.items():
                construction.append(f'<optgroup label="{group}">')
                for key, value in group_dict.items():
                    if value == selected:
                        construction.append(f'<option value="{value}">{key}</option>')
                    construction.append(f'<option value="{value}">{key}</option>')
                construction.append('</optgroup>')

        construction.append('</select>')

        if prepend_label != "":
            construction = self.prepend_label_func(construction, prepend_label)

        if append_label != "":
            construction = self.append_label_func(construction, prepend_label)

        if prepend_button != "":
            construction = self.prepend_button_func(construction, prepend_button)

        if append_button != "":
            construction = self.append_button_func(construction, append_button)

        if label != "":
            construction.insert(0, f'<label for="{_name}" class="mb-2">{_label}</label>')

        final = self.wrap_element(construction, wrap_class, wrap_inner_class)
        return Markup("".join(final))
