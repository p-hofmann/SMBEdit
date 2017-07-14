__author__ = 'Peter Hofmann'


# from smbeditGUI import SMBEditGUI
from ..frames.rootframe import RootFrame


class ActionMoveCenter(RootFrame):
    """
    @type _smbedit: SMBEditGUI
    """
    def __init__(self, master, smbedit):
        self._smbedit = smbedit
        super(ActionMoveCenter, self).__init__(master, smbedit)

        self.main_frame.tool.tool_move_center.button_block_id.configure(command=self.button_press_block_id)
        self.main_frame.tool.tool_move_center.button_vector.configure(command=self.button_press_vector)

    def button_press_block_id(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].move_center_by_block_id(
            int(self.main_frame.tool.tool_move_center.variable_block_id.get()))

    def button_press_vector(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].move_center_by_vector(
            (
                int(self.main_frame.tool.tool_move_center.variable_x.get()),
                int(self.main_frame.tool.tool_move_center.variable_y.get()),
                int(self.main_frame.tool.tool_move_center.variable_z.get()))
            )
