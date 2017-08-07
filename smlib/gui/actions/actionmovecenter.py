from .actiondefault import ActionDefault


class ActionMoveCenter(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionMoveCenter, self).__init__(main_frame=main_frame, smbedit=smbedit)

    def button_press_block_id(self):
        self._main_frame.status_bar.showMessage("Moving center/core to specific block id ...".format())
        try:
            current_index = self._main_frame.entities_combo_box.currentIndex()
            index = self.block_id_combobox.currentIndex()
            block_id = self.block_id_combobox.itemData(index)
            self._smbedit.blueprint[current_index].move_center_by_block_id(block_id)
            self._main_frame.update_summary()
            self._main_frame.status_bar.showMessage("Moving center/core to specific block id ... Done!".format())
        except AssertionError as e:
            self._main_frame.status_bar.showMessage("{}".format(e))

    def button_press_vector(self):
        try:
            x = int(self.variable_x.text())
            y = int(self.variable_y.text())
            z = int(self.variable_z.text())
        except:
            self._main_frame.status_bar.showMessage("Error: Bad value.".format())
            return

        current_index = self._main_frame.entities_combo_box.currentIndex()
        self._main_frame.status_bar.showMessage("Moving center/core by vector ...".format())
        self._smbedit.blueprint[current_index].move_center_by_vector((x, y, z))
        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Moving center/core by vector ... Done!".format())
