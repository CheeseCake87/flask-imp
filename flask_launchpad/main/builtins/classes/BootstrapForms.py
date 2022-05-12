from markupsafe import Markup


class BootstrapForms:
    def __init__(self):
        _version = "0.1"

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
        _constructor = constructor
        _constructor.insert(0, '<div class="input-group">')
        _constructor.append('</div>')
        return _constructor

    def prepend_label_func(self, constructor: list, label: str) -> list:
        _constructor = constructor
        if '<div class="input-group">' not in _constructor:
            _constructor = self.apply_input_group(_constructor)
        _constructor.insert(1, f'</div>')
        _constructor.insert(1,
                            f'<span class="input-group-text" id="inputGroup-sizing-default">{label}</span>')
        _constructor.insert(1, f'<div class="input-group-prepend">')
        print(_constructor)
        return _constructor

    def append_label_func(self, constructor: list, label: str) -> list:
        _constructor = constructor
        if '<div class="input-group">' not in _constructor:
            _constructor = self.apply_input_group(_constructor)
        _constructor.append(f'<div class="input-group-append">')
        _constructor.append(
            f'<span class="input-group-text" id="inputGroup-sizing-default">{label}</span>')
        _constructor.append(f'</div>')
        return _constructor

    def prepend_button_func(self, constructor: list, button_object: str) -> list:
        _constructor = constructor
        if '<div class="input-group">' not in _constructor:
            _constructor = self.apply_input_group(_constructor)
        _constructor.insert(1, f'</div>')
        _constructor.insert(1, button_object)
        _constructor.insert(1, f'<div class="input-group-prepend">')
        _constructor.insert(1, f'<div class="input-group">')
        _constructor.append('</div>')
        return _constructor

    def append_button_func(self, constructor: list, button_object: str) -> list:
        _constructor = constructor
        if '<div class="input-group">' not in _constructor:
            _constructor.append(f'<div class="input-group-append">')
            _constructor.append(button_object)
            _constructor.append(f'</div>')
            _constructor = self.apply_input_group(_constructor)
            return _constructor

        _constructor.insert(_constructor.__len__() - 1, f'<div class="input-group-append">')
        _constructor.insert(_constructor.__len__() - 1, button_object)
        _constructor.append(f'</div>')
        return _constructor

    def hidden(self,
               name: str,
               value: str
               ):
        return Markup(
            f'<input type="hidden" name="{self.no_space(name)}" id="{self.no_space(name)}" value="{value}" />')

    def button(self,
               label: str,
               element_type: str = "button",
               button_action: str = "button",
               button_class: str = None,
               href: str = "#",
               wrap_class: str = None,
               wrap_inner_class: str = None,
               disabled: bool = False,
               ) -> str:
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
            construction.append(f'class="{button_class} ')
            if disabled:
                construction.append('disabled')
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
                construction.append('disabled"')
            construction.append(f'>{label}</button>')
            final = self.wrap_element(construction, wrap_class, wrap_inner_class)
            return Markup("".join(final))

        construction.append("<p>Not a valid element type</p>")
        return Markup("".join(construction))

    def input(self,
              name: str,
              label: str = "",
              prepend_label: str = "",
              append_label: str = "",
              prepend_button: str = "",
              append_button: str = "",
              placeholder: str = "",
              input_type: str = "text",
              input_class: str = "",
              wrap_class: str = None,
              wrap_inner_class: str = None,
              required: bool = False,
              readonly: bool = False,
              disabled: bool = False,
              multiple: bool = False,
              value: str = None,
              ) -> str:

        _name = self.no_space(name)
        _label = self.title(label)

        construction = [
            f'<input ',
            f'type="{input_type}" ',
            f'name="{_name}" ',
            f'id="{_name}" ',
            f'class="form-control {input_class}" ',
        ]

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
               name: str,
               label: str = "",
               prepend_label: str = "",
               append_label: str = "",
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
            f'class="form-control {input_class}" ',
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

        if label != "":
            construction.insert(0, f'<label for="{_name}">{_label}</label>')

        final = self.wrap_element(construction, wrap_class, wrap_inner_class)
        return Markup("".join(final))
