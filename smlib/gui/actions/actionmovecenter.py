__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionMoveCenter(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionMoveCenter, self).__init__(main_frame=main_frame, smbedit=smbedit)
        ActionMoveCenter.set_commands(self)

    def set_commands(self):
        """
        Set commands of components
        """
        self._main_frame.tool.tool_move_center.button_block_id.configure(command=self.button_press_block_id)
        self._main_frame.tool.tool_move_center.button_vector.configure(command=self.button_press_vector)

    def button_press_block_id(self):
        self._main_frame.status_bar.set("Moving center/core to specific block id ...".format())
        try:
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].move_center_by_block_id(
                self._main_frame.tool.tool_move_center.variable_block_id.get())
            self._main_frame.update_summary(self._smbedit)
            self._main_frame.status_bar.set("Moving center/core to specific block id ... Done!".format())
        except AssertionError as e:
            self._main_frame.status_bar.set("{}".format(e))

    def button_press_vector(self):
        self._main_frame.status_bar.set("Moving center/core by vector ...".format())
        self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].move_center_by_vector(
            (
                self._main_frame.tool.tool_move_center.variable_x.get(),
                self._main_frame.tool.tool_move_center.variable_y.get(),
                self._main_frame.tool.tool_move_center.variable_z.get())
            )
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Moving center/core by vector ... Done!".format())
