__author__ = 'Peter Hofmann'


# from smbeditGUI import SMBEditGUI
from lib.gui.frames.rootframe import RootFrame


class ActionMiscellaneous(RootFrame):
    """
    @type _smbedit: SMBEditGUI
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

    def __init__(self, master, smbedit):
        self._smbedit = smbedit
        super(ActionMiscellaneous, self).__init__(master, smbedit)

        self.main_frame.tool.tool_else.combo_box_type.bind("<<ComboboxSelected>>", self.combo_box_type_change)
        self.main_frame.tool.tool_else.combo_box_class.bind("<<ComboboxSelected>>", self.combo_box_class_change)
        self.refresh_combobox_values()

    def combo_box_type_change(self, event):
        self.refresh_combobox_values()
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].set_entity(
            self.main_frame.tool.tool_else.combo_box_type.current(),
            self.main_frame.tool.tool_else.combo_box_class.current())

    def combo_box_class_change(self, event):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].set_entity(
            self.main_frame.tool.tool_else.combo_box_type.current(),
            self.main_frame.tool.tool_else.combo_box_class.current())

    def refresh_combobox_values(self):
        if self.main_frame.tool.tool_else.combo_box_type.current() == 0:
            self.main_frame.tool.tool_else.combo_box_class['values'] = list(self._ct_to_ship_class.values())
        elif self.main_frame.tool.tool_else.combo_box_type.current() == 2:
            self.main_frame.tool.tool_else.combo_box_class['values'] = list(self._ct_to_station_class.values())
        else:
            self.main_frame.tool.tool_else.combo_box_class['values'] = ["General"]
        self.main_frame.tool.tool_else.combo_box_class.current(0)
