__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk
from .tools.frametool import FrameTool
from .summary.framesummary import FrameSummary
from .rootframe import RootFrame
from ...utils.blockconfig import block_config


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

        self.disable()

    # #################
    # GUI
    # #################

    def _gui_combobox_blueprint(self, root_frame):
        """
        @type root_frame: MainFrame
        """
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
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        if len(self.list_of_entity_names) == 0:
            return
        self.summary.text_box.delete()

        self.update_header(smbedit)
        self.update_logic(smbedit)
        self.update_metadata(smbedit)
        self.update_smd(smbedit)

    def update_header(self, smbedit):
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
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

    def update_logic(self, smbedit):
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
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

    def update_metadata(self, smbedit):
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        self.summary.text_box.write("# Metadata v{}\n".format(
            smbedit.blueprint[self.entities_combo_box.current()].meta._version))

        self.summary.text_box.write("\n")

    def update_smd(self, smbedit):
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        self.summary.text_box.write("# SMD\n")
        self.summary.text_box.write("\tNumber of Blocks: ")
        if self.entities_variable_checkbox.get():
            self.summary.text_box.write("{}\n".format(
                smbedit.blueprint[self.entities_combo_box.current()].smd3.get_number_of_blocks()))
            block_id_to_quantity = smbedit.blueprint[self.entities_combo_box.current()].smd3.get_block_id_to_quantity()
        else:
            total_sum = 0
            block_id_to_quantity = {}
            for blueprint in smbedit.blueprint:
                total_sum += blueprint.smd3.get_number_of_blocks()
                for block_id, quantity in blueprint.smd3.get_block_id_to_quantity().items():
                    if block_id not in block_id_to_quantity:
                        block_id_to_quantity[block_id] = 0
                    block_id_to_quantity[block_id] += quantity
            self.summary.text_box.write("{}\n".format(total_sum))

        self.summary.text_box.write("\n")

        for block_id, quantity in block_id_to_quantity.items():
            self.summary.text_box.write("\t{}:\t{}\n".format(quantity, block_config[block_id].name))

        self.summary.text_box.write("\n")

    def disable(self):
        self.entities_combo_box.config(state=tk.DISABLED)
        self.entities_check_box.config(state=tk.DISABLED)
        self.summary.disable()
        self.tool.disable()

    def enable(self):
        self.entities_combo_box.config(state=tk.NORMAL)
        self.entities_check_box.config(state=tk.NORMAL)
        self.summary.enable()
        self.tool.enable()
