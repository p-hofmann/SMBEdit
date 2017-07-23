__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionMirror(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionMirror, self).__init__(main_frame=main_frame, smbedit=smbedit)
        ActionMirror.set_commands(self)

    def set_commands(self):
        """
        Set commands of components
        """
        self._main_frame.tool.tool_mirror.button_mirror.configure(command=self.button_press_mirror)

    def button_press_mirror(self):
        if self._main_frame.entities_variable_checkbox.get():
            self._main_frame.status_bar.set("Mirroring entity ...".format())
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].mirror_axis(
                self._main_frame.tool.tool_mirror.variable_radiobox_axis.get(),
                self._main_frame.tool.tool_mirror.variable_checkbox_reversed.get()
                )
        else:
            self._main_frame.status_bar.set("Mirroring main entity ...".format())
            self._smbedit.blueprint[0].mirror_axis(
                self._main_frame.tool.tool_mirror.variable_radiobox_axis.get(),
                self._main_frame.tool.tool_mirror.variable_checkbox_reversed.get()
                )
        #     for blueprint in self._smbedit.blueprint:
        #         blueprint.mirror_axis(
        #             self._main_frame.tool.tool_mirror.variable_radiobox_axis.get(),
        #             self._main_frame.tool.tool_mirror.variable_checkbox_reversed.get()
        #             )
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Mirroring ... Done!".format())