__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk
from lib.gui.frames.tools.frametool import FrameTool


class MainFrame(tk.Frame):
    """
    @type combo_box_entities: ttk.Combobox
    @type tool: FrameTool
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self._current_index = 0
        self._gui_combobox_blueprint(self)

        self.tool = FrameTool(self)
        self.tool.pack(side=tk.TOP, fill=tk.X)

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
            root_frame, text="Entity")  # , relief=tk.RAISED
        # frame.pack(side=tk.RIGHT, fill=tk.Y)
        frame.pack(side=tk.TOP, fill=tk.X)

        self.combo_box_entities = ttk.Combobox(frame, textvariable=self.box_value, state='readonly')
        self.combo_box_entities.pack(fill=tk.X)
        self.combo_box_entities['values'] = ['N/A']
        self.combo_box_entities.current(0)
        # self._combo_box.bind("<<ComboboxSelected>>", self.newselection)
        # box.grid(column=0, row=0)

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
