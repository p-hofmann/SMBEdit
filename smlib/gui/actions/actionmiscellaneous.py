from .actiondefault import ActionDefault


class ActionMiscellaneous(ActionDefault):
    """
    Dealing with component interactions

    @type _ct_to_ship_class: dict[int, str]
    @type _ct_to_station_class: dict[int, str]
    """

    _ct_to_ship_class = {
        0: "General",  #
        1: "Mining",  #
        2: "Support",  #
        3: "Cargo",  #
        4: "Attack",  #
        5: "Defence",  #
        6: "Carrier",  #
        7: "Scout",  #
        8: "Scavenger",  #
    }

    _ct_to_station_class = {
        0: "General",  #
        1: "Mining",  #
        2: "Trade",  #
        3: "Shopping",  #
        4: "Outpost",  #
        5: "Defence",  #
        6: "Shipyard",  #
        7: "Warp Gate",  #
        8: "Factory",  #
    }

    def __init__(self, main_frame, smbedit):
        super(ActionMiscellaneous, self).__init__(main_frame=main_frame, smbedit=smbedit)
        self.combo_box_type = None
        self.combo_box_class = None

    def combo_box_type_change(self, type_index):
        if type_index == -1:
            return
        self.refresh_combobox_values()

    def on_click_confirm(self):
        self._smbedit.blueprint[self._main_frame.entities_combo_box.currentIndex()].set_entity(
            self.combo_box_type.currentIndex(),
            self.combo_box_class.currentIndex())
        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Entity type/class changed!".format())

    def refresh_combobox_values(self):
        if self.combo_box_type.currentIndex() == 0:
            self.combo_box_class.clear()
            self.combo_box_class.insertItems(0, list(self._ct_to_ship_class.values()))
        elif self.combo_box_type.currentIndex() == 2:
            self.combo_box_class.clear()
            self.combo_box_class.insertItems(0, list(self._ct_to_station_class.values()))
        else:
            self.combo_box_class.clear()
            self.combo_box_class.addItem("General")
