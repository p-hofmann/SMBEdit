__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionReplace(ActionDefault):
    """
    Dealing with component interactions
    """

    def set_commands(self):
        """
        Set commands of components
        """
        self._main_frame.tool.tool_replace.button_remove.configure(command=self.button_press_remove)
        self._main_frame.tool.tool_replace.button_replace_block.configure(command=self.button_press_replace_block)
        self._main_frame.tool.tool_replace.button_replace_hull.configure(command=self.button_press_replace_hull)

    def button_press_remove(self):
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].remove_blocks(
                set(int(self._main_frame.tool.tool_replace.variable_remove.get())))
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.remove_blocks(
                    set(int(self._main_frame.tool.tool_replace.variable_remove.get())))

    def button_press_replace_block(self):
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

    def button_press_replace_hull(self):
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
