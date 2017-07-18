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
        note.pack(side=tk.TOP, fill=tk.X)

        self.summary = FrameSummary(note)
        self.summary.pack(side=tk.TOP, fill=tk.X)
        note.add(self.summary, text="Summary")

        self.tool = FrameTool(note)
        self.tool.pack(side=tk.TOP, fill=tk.X)
        note.add(self.tool, text="Tools")

    # #################
    # GUI
    # #################

    # def newselection(self, event):
    #     self._current_index = self._combo_box.current()
    #     # self.value_of_combo = self.box.current()
    #     # print(self.value_of_combo)

    def _gui_combobox_blueprint(self, root_frame):
        self.box_value = tk.StringVar()
        frame = tk.LabelFrame(
            root_frame, text="Specific Entity")  # , relief=tk.RAISED
        # frame.pack(side=tk.RIGHT, fill=tk.Y)
        frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.entities_variable_checkbox = tk.BooleanVar()

        self.entities_check_box = tk.Checkbutton(
            frame, text="", variable=self.entities_variable_checkbox,
            command=self.entities_check_box_onchange,
            onvalue=True, offvalue=False)
        self.entities_check_box.pack(fill=tk.X, side=tk.LEFT)

        self.entities_combo_box = ttk.Combobox(frame, textvariable=self.box_value, state='readonly')
        self.entities_combo_box.pack(fill=tk.X)
        self.entities_combo_box['values'] = ['All']
        self.entities_combo_box.current(0)
        # self._combo_box.bind("<<ComboboxSelected>>", self.newselection)
        # box.grid(column=0, row=0)

    def entities_check_box_onchange(self):
        # if :
        if not self.entities_variable_checkbox.get():
            self.entities_combo_box['values'] = ['All']
        elif len(self.list_of_entity_names) > 0:
            self.entities_combo_box['values'] = self.list_of_entity_names
        self.entities_combo_box.current(0)

# frame = tk.LabelFrame(self._root, text="Output")
# frame.pack(side=tk.BOTTOM)
# frame.grid_propagate(False)
# implement stretchability
# frame.grid_rowconfigure(0, weight=1)
# frame.grid_columnconfigure(0, weight=1)
# text_box = tk.Text(frame, wrap='word', height=5, width=100, state=tk.DISABLED)
# text_box.pack(fill=tk.BOTH, expand=1)
# scrollb = tk.Scrollbar(frame, command=text_box.yview)
# scrollb.grid(row=0, column=1, sticky='nsew')
# text_box['yscrollcommand'] = scrollb.set
# self.text_box = StreamToTkText(text_box)
