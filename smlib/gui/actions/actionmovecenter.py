__author__ = 'Peter Hofmann'


# from smbeditGUI import SMBEditGUI


class ActionMoveCenter(object):
    """
    @type _smbedit: smbeditGUI.SMBEditGUI
    """
    def __init__(self, main_frame, smbedit):
        """

        @type main_frame: smlib.gui.frames.mainframe.MainFrame
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        self._smbedit = smbedit
        self.main_frame = main_frame

        self.main_frame.tool.tool_move_center.button_block_id.configure(command=self.button_press_block_id)
        self.main_frame.tool.tool_move_center.button_vector.configure(command=self.button_press_vector)

    def button_press_block_id(self):
        self._smbedit.blueprint[self.main_frame.entities_combo_box.current()].move_center_by_block_id(
            int(self.main_frame.tool.tool_move_center.variable_block_id.get()))

    def button_press_vector(self):
        self._smbedit.blueprint[self.main_frame.entities_combo_box.current()].move_center_by_vector(
            (
                int(self.main_frame.tool.tool_move_center.variable_x.get()),
                int(self.main_frame.tool.tool_move_center.variable_y.get()),
                int(self.main_frame.tool.tool_move_center.variable_z.get()))
            )
