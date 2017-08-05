__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionMirror(ActionDefault):
    """
    Dealing with component interactions

    @type _main_frame: smlib.gui.frames.mainframe.MainFrame
    @type _smbedit: smbeditGUI.SMBEditGUI
    """

    def __init__(self, main_frame, smbedit):
        super(ActionMirror, self).__init__(main_frame=main_frame, smbedit=smbedit)

    def button_press_mirror(self):
        if self._main_frame.entities_check_box.isChecked():
            self._main_frame.status_bar.showMessage("Mirroring entity ...".format())
            self._smbedit.blueprint[self._main_frame.entities_combo_box.currentIndex()].mirror_axis(
                self._main_frame.tool.tool_mirror.button_group.checkedId(),
                self._main_frame.tool.tool_mirror.check_button.isChecked()
                )
        else:
            self._main_frame.status_bar.showMessage("Mirroring main entity ...".format())
            self._smbedit.blueprint[0].mirror_axis(
                self._main_frame.tool.tool_mirror.button_group.checkedId(),
                self._main_frame.tool.tool_mirror.check_button.isChecked()
                )
        #     for blueprint in self._smbedit.blueprint:
        #         blueprint.mirror_axis(
        #             self._main_frame.tool.tool_mirror.variable_radiobox_axis.get(),
        #             self._main_frame.tool.tool_mirror.variable_checkbox_reversed.get()
        #             )
        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Mirroring ... Done!".format())
