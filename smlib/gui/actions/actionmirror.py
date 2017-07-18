__author__ = 'Peter Hofmann'


# from smbeditGUI import SMBEditGUI


class ActionMirror(object):
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
        self.main_frame.tool.tool_mirror.button_mirror.configure(command=self.button_press_mirror)

    def button_press_mirror(self):
        self._smbedit.blueprint[self.main_frame.entities_combo_box.current()].mirror_axis(
            self.main_frame.tool.tool_mirror.variable_radiobox_axis.get(),
            self.main_frame.tool.tool_mirror.variable_checkbox_reversed.get()
            )
