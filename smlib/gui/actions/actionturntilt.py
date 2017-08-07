from .actiondefault import ActionDefault


class ActionTurnTilt(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionTurnTilt, self).__init__(main_frame=main_frame, smbedit=smbedit)

    def button_press(self, turn_tilt_index):
        if self._main_frame.entities_check_box.isChecked():
            current_index = self._main_frame.entities_combo_box.currentIndex()
            self._main_frame.status_bar.showMessage("Turning entity ...".format())
            self._smbedit.blueprint[current_index].turn_tilt(turn_tilt_index)
            self._main_frame.status_bar.showMessage("Turning ... Done!".format())
        else:
            self._main_frame.status_bar.showMessage("Turning main entity ...".format())
            self._smbedit.blueprint[0].turn_tilt(turn_tilt_index)
            self._main_frame.status_bar.showMessage("Turning main entity ... Done!".format())
        self._main_frame.update_summary()

