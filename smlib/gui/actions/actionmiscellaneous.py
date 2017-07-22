__author__ = 'Peter Hofmann'


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
        ActionMiscellaneous.set_commands(self)

    def set_commands(self):
        """
        Set commands of components
        """
        self._main_frame.tool.tool_else.combo_box_type.bind("<<ComboboxSelected>>", self.combo_box_type_change)
        self._main_frame.tool.tool_else.combo_box_class.bind("<<ComboboxSelected>>", self.combo_box_class_change)
        self.refresh_combobox_values()

    def combo_box_type_change(self, event):
        self.refresh_combobox_values()
        self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].set_entity(
            self._main_frame.tool.tool_else.combo_box_type.current(),
            self._main_frame.tool.tool_else.combo_box_class.current())
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Entity type changed!".format())

    def combo_box_class_change(self, event):
        self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].set_entity(
            self._main_frame.tool.tool_else.combo_box_type.current(),
            self._main_frame.tool.tool_else.combo_box_class.current())
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Entity class changed!".format())

    def refresh_combobox_values(self):
        if self._main_frame.tool.tool_else.combo_box_type.current() == 0:
            self._main_frame.tool.tool_else.combo_box_class['values'] = list(self._ct_to_ship_class.values())
        elif self._main_frame.tool.tool_else.combo_box_type.current() == 2:
            self._main_frame.tool.tool_else.combo_box_class['values'] = list(self._ct_to_station_class.values())
        else:
            self._main_frame.tool.tool_else.combo_box_class['values'] = ["General"]
        self._main_frame.tool.tool_else.combo_box_class.current(0)
