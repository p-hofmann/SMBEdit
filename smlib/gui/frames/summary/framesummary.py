__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk
from smlib.gui.frames.streamtotktext import StreamToTkText


class FrameSummary(tk.LabelFrame):
    """
    @type text_box: StreamToTkText
    """

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text="Summary")

        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, padx=2, pady=2, expand=tk.TRUE, fill=tk.BOTH)
        frame.grid_propagate(False)
        # implement stretchability
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        text_box = tk.Text(frame, wrap='word', state=tk.DISABLED, width=50)  # , height=5
        text_box.pack(fill=tk.BOTH, expand=tk.TRUE)
        scrollb = tk.Scrollbar(frame, command=text_box.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        text_box['yscrollcommand'] = scrollb.set
        self.text_box = StreamToTkText(text_box)

    def disable(self):
        pass

    def enable(self):
        pass