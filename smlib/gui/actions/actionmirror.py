__author__ = 'Peter Hofmann'


# from smbeditGUI import SMBEditGUI
from smlib.gui import RootFrame


class ActionMirror(RootFrame):
    """
    @type _smbedit: SMBEditGUI
    """
    def __init__(self, master, smbedit):
        self._smbedit = smbedit
        super(ActionMirror, self).__init__(master, smbedit)

        self.main_frame.tool.tool_mirror.button_mirror.configure(command=self.button_press_mirror)

    def button_press_mirror(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].mirror_axis(
            self.main_frame.tool.tool_mirror.variable_radiobox_axis.get(),
            self.main_frame.tool.tool_mirror.variable_checkbox_reversed.get()
            )
