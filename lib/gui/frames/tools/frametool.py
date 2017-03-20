__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk
from lib.gui.frames.tools.frameautoshape import FrameAutoShape
from lib.gui.frames.tools.framemovecenter import FrameMoveCenter
from lib.gui.frames.tools.framereplace import FrameReplace
from lib.gui.frames.tools.framemirror import FrameMirror
from lib.gui.frames.tools.framemiscellaneous import FrameMiscellaneous


class FrameTool(tk.Frame):
    """
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)  # , text="Tools"

        some_frame = tk.Frame(self)
        self.auto_shape = FrameAutoShape(some_frame)
        self.auto_shape.pack(side=tk.TOP, fill=tk.X, pady=2)

        self.tool_mirror = FrameMirror(some_frame)
        self.tool_mirror.pack(side=tk.TOP, pady=2)
        some_frame.pack(side=tk.LEFT, fill=tk.Y)

        some_frame = tk.Frame(self)
        self.tool_move_center = FrameMoveCenter(some_frame)
        self.tool_move_center.pack(side=tk.TOP, pady=2)

        self.tool_else = FrameMiscellaneous(some_frame)
        self.tool_else.pack(side=tk.TOP, fill=tk.X, pady=2)
        some_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.tool_replace = FrameReplace(self)
        self.tool_replace.pack(side=tk.LEFT)

        # blueprint.to_stream()

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
