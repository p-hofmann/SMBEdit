__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionMoveCenter(ActionDefault):
    """
    Dealing with component interactions
    """

    def set_commands(self):
        """
        Set commands of components
        """
        self._main_frame.tool.tool_move_center.button_block_id.configure(command=self.button_press_block_id)
        self._main_frame.tool.tool_move_center.button_vector.configure(command=self.button_press_vector)

    def button_press_block_id(self):
        self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].move_center_by_block_id(
            int(self._main_frame.tool.tool_move_center.variable_block_id.get()))

    def button_press_vector(self):
        self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].move_center_by_vector(
            (
                int(self._main_frame.tool.tool_move_center.variable_x.get()),
                int(self._main_frame.tool.tool_move_center.variable_y.get()),
                int(self._main_frame.tool.tool_move_center.variable_z.get()))
            )
