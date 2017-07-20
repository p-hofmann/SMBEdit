__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk
from smlib.gui.frames.streamtotktext import StreamToTkText


class FrameSummary(tk.Frame):
    """
    @type text_box: StreamToTkText
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)  # , text="Tools"

        self.draw_summary()

    def draw_summary(self):
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, padx=5, pady=5, expand=tk.TRUE, fill=tk.BOTH)
        frame.grid_propagate(False)
        # implement stretchability
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        text_box = tk.Text(frame, wrap='word', state=tk.DISABLED)  # , height=5, width=100
        text_box.pack(fill=tk.BOTH, expand=tk.TRUE)
        scrollb = tk.Scrollbar(frame, command=text_box.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        text_box['yscrollcommand'] = scrollb.set
        self.text_box = StreamToTkText(text_box)
