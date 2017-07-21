__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionMirror(ActionDefault):
    """
    Dealing with component interactions
    """

    def set_commands(self):
        """
        Set commands of components
        """
        self._main_frame.tool.tool_mirror.button_mirror.configure(command=self.button_press_mirror)

    def button_press_mirror(self):
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].mirror_axis(
                self._main_frame.tool.tool_mirror.variable_radiobox_axis.get(),
                self._main_frame.tool.tool_mirror.variable_checkbox_reversed.get()
                )
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.mirror_axis(
                    self._main_frame.tool.tool_mirror.variable_radiobox_axis.get(),
                    self._main_frame.tool.tool_mirror.variable_checkbox_reversed.get()
                    )
