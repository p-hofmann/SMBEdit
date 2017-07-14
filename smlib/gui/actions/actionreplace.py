__author__ = 'Peter Hofmann'


# from smbeditGUI import SMBEditGUI
from ..frames.rootframe import RootFrame


class ActionReplace(RootFrame):
    """
    @type _smbedit: SMBEditGUI
    """
    def __init__(self, master, smbedit):
        self._smbedit = smbedit
        super(ActionReplace, self).__init__(master, smbedit)

        self.main_frame.tool.tool_replace.button_remove.configure(command=self.button_press_remove)
        self.main_frame.tool.tool_replace.button_replace_block.configure(command=self.button_press_replace_block)
        self.main_frame.tool.tool_replace.button_replace_hull.configure(command=self.button_press_replace_hull)

    def button_press_remove(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].remove_blocks(
            set(int(self.main_frame.tool.tool_replace.variable_remove.get())))

    def button_press_replace_block(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].replace_blocks(
            int(self.main_frame.tool.tool_replace.variable_block_original.get()),
            int(self.main_frame.tool.tool_replace.variable_block_replacement.get())
            )

    def button_press_replace_hull(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].replace_blocks(
            self.main_frame.tool.tool_replace.ariable_hull_original.get(),
            self.main_frame.tool.tool_replace.variable_hull_replacement.get()
            )
