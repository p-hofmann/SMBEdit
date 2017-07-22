__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk
from ....utils.blueprintentity import BlueprintEntity


class FrameMiscellaneous(tk.LabelFrame):
    """
    @type combo_box_type: ttk.Combobox
    @type combo_box_class: ttk.Combobox
    """

    def __init__(self, master):
        """
        """
        tk.LabelFrame.__init__(self, master, text="Miscellaneous")
        self._gui_entity_type()
        self._gui_entity_class()
        # blueprint.set_entity(self._entity_type, self._entity_class)
        # blueprint.link_salvage_modules()
        # blueprint.update()

    def _gui_entity_type(self):
        frame = tk.LabelFrame(
            self, text="Type")  # , relief=tk.RAISED
        # frame.pack(side=tk.RIGHT, fill=tk.Y)
        frame.pack(side=tk.TOP, fill=tk.X, pady=2, padx=2)

        self.combo_box_type = ttk.Combobox(frame, state='readonly')
        self.combo_box_type.pack(fill=tk.X, pady=2, padx=5)
        self.combo_box_type['values'] = list(BlueprintEntity.entity_types.values())
        self.combo_box_type.current(0)
        # self.combo_box.bind("<<ComboboxSelected>>", self.newselection)
        # box.grid(column=0, row=0)

    def _gui_entity_class(self):
        frame = tk.LabelFrame(
            self, text="Class")  # , relief=tk.RAISED
        # frame.pack(side=tk.RIGHT, fill=tk.Y)
        frame.pack(side=tk.TOP, fill=tk.X, pady=1, padx=2)

        self.combo_box_class = ttk.Combobox(frame, state='readonly')
        # self.combo_box_class['values'] = list(self._ct_to_ship_class.values())
        self.combo_box_class['values'] = ["General"]
        self.combo_box_class.current(0)
        self.combo_box_class.pack(fill=tk.X, pady=1, padx=5)
        # box.grid(column=0, row=0)

    def disable(self):
        self.combo_box_type.config(state=tk.DISABLED)
        self.combo_box_class.config(state=tk.DISABLED)

    def enable(self):
        self.combo_box_type.config(state=tk.NORMAL)
        self.combo_box_class.config(state=tk.NORMAL)
