__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk
from .tools.frametool import FrameTool
from .framesummary import FrameSummary
from .rootframe import RootFrame


class MainFrame(RootFrame):
    """
    @type entities_combo_box: ttk.Combobox
    @type tool: FrameTool
    @type summary: FrameSummary
    """

    def __init__(self, root):
        RootFrame.__init__(self, root)
        # tk.Frame.__init__(self, master)

        self._current_index = 0
        self.list_of_entity_names = []
        self._gui_combobox_blueprint(self)

        note = ttk.Notebook(self)
        note.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, pady=5)

        self.summary = FrameSummary(note)
        self.summary.pack(side=tk.TOP, fill=tk.BOTH)
        note.add(self.summary, text="Summary")

        self.tool = FrameTool(note)
        self.tool.pack(side=tk.TOP, fill=tk.BOTH)
        note.add(self.tool, text="Tools")

    # #################
    # GUI
    # #################

    def _gui_combobox_blueprint(self, root_frame):
        self.box_value = tk.StringVar()
        frame = tk.LabelFrame(
            root_frame, text="Specific Entity")  # , relief=tk.RAISED
        frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.entities_variable_checkbox = tk.BooleanVar()

        self.entities_check_box = tk.Checkbutton(
            frame, text="", variable=self.entities_variable_checkbox,
            # command=self.entities_check_box_onchange,
            onvalue=True, offvalue=False)
        self.entities_check_box.pack(fill=tk.X, side=tk.LEFT)

        self.entities_combo_box = ttk.Combobox(frame, textvariable=self.box_value, state='readonly')
        self.entities_combo_box.pack(fill=tk.X)
        self.entities_combo_box['values'] = ['All']
        self.entities_combo_box.current(0)

    def update_summary(self, smbedit):
        if len(self.list_of_entity_names) == 0:
            return
        self.summary.text_box.delete()
        self.summary.text_box.write("# Header v{}\n".format(
            smbedit.blueprint[self.entities_combo_box.current()].header.version))
        self.summary.text_box.write("\tLength: {}, Width: {}, Height: {}, \n".format(
            round(smbedit.blueprint[self.entities_combo_box.current()].header.get_length()),
            round(smbedit.blueprint[self.entities_combo_box.current()].header.get_width()),
            round(smbedit.blueprint[self.entities_combo_box.current()].header.get_height()),
            ))
        self.summary.text_box.write("\tType: {}\n".format(
            smbedit.blueprint[self.entities_combo_box.current()].header.get_type_name()))
        self.summary.text_box.write("\tRole: {}\n".format(
            smbedit.blueprint[self.entities_combo_box.current()].header.get_classification_name()))

        self.summary.text_box.write("\n")

        controller_version = 0
        tmp = smbedit.blueprint[self.entities_combo_box.current()].logic._controller_version
        if tmp < -1:
            controller_version = abs(tmp) - 1024
        self.summary.text_box.write("# Logic v{}.{}\n".format(
            smbedit.blueprint[self.entities_combo_box.current()].logic.version,
            controller_version
            ))
        self.summary.text_box.write("\tControllers: {}\n".format(
            len(smbedit.blueprint[self.entities_combo_box.current()].logic._controller_position_to_block_id_to_block_positions)))

        self.summary.text_box.write("\n")

        self.summary.text_box.write("# Metadata v{}\n".format(
            smbedit.blueprint[self.entities_combo_box.current()].meta._version))

        self.summary.text_box.write("\n")

        self.summary.text_box.write("# SMD\n")
        if self.entities_variable_checkbox.get():
            self.summary.text_box.write("\tBlocks: {}\n".format(
                len(smbedit.blueprint[self.entities_combo_box.current()].smd3._block_list)))
        else:
            total_sum = 0
            for blueprint in smbedit.blueprint:
                total_sum += len(blueprint.smd3._block_list)
            self.summary.text_box.write("\tBlocks: {}\n".format(
                total_sum))
