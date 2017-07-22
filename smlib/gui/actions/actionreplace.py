__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionReplace(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionReplace, self).__init__(main_frame=main_frame, smbedit=smbedit)
        ActionReplace.set_commands(self)

    def set_commands(self):
        """
        Set commands of components
        """
        # print("ActionReplace")
        self._main_frame.tool.tool_replace.button_remove.configure(command=self.button_press_remove)
        self._main_frame.tool.tool_replace.button_replace_block.configure(command=self.button_press_replace_block)
        self._main_frame.tool.tool_replace.button_replace_hull.configure(command=self.button_press_replace_hull)

    def button_press_remove(self):
        self._main_frame.status_bar.set("Removing blocks ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].remove_blocks(
                set(int(self._main_frame.tool.tool_replace.variable_remove.get())))
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.remove_blocks(
                    set(int(self._main_frame.tool.tool_replace.variable_remove.get())))
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Removing blocks ... Done!".format())

    def button_press_replace_block(self):
        self._main_frame.status_bar.set("Replacing blocks ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].replace_blocks(
                int(self._main_frame.tool.tool_replace.variable_block_original.get()),
                int(self._main_frame.tool.tool_replace.variable_block_replacement.get())
                )
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.replace_blocks(
                    int(self._main_frame.tool.tool_replace.variable_block_original.get()),
                    int(self._main_frame.tool.tool_replace.variable_block_replacement.get())
                    )
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Replacing blocks ... Done!".format())

    def button_press_replace_hull(self):
        self._main_frame.status_bar.set("Replacing hull blocks ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].replace_blocks(
                self._main_frame.tool.tool_replace.ariable_hull_original.get(),
                self._main_frame.tool.tool_replace.variable_hull_replacement.get()
                )
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.replace_blocks(
                    self._main_frame.tool.tool_replace.ariable_hull_original.get(),
                    self._main_frame.tool.tool_replace.variable_hull_replacement.get()
                    )
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Replacing hull blocks ... Done!".format())
