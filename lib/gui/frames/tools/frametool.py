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


class FrameTool(tk.LabelFrame):
    """
    """

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text="Tools")

        self.auto_shape = FrameAutoShape(self)
        self.auto_shape.pack(side=tk.LEFT)

        self.tool_move_center = FrameMoveCenter(self)
        self.tool_move_center.pack(side=tk.LEFT)

        self.tool_replace = FrameReplace(self)
        self.tool_replace.pack(side=tk.LEFT)

        self.tool_mirror = FrameMirror(self)
        self.tool_mirror.pack(side=tk.LEFT)

        self.tool_else = FrameMiscellaneous(self)
        self.tool_else.pack(side=tk.LEFT)

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
