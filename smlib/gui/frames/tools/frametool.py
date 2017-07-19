__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk
from ...frames.tools.frameautoshape import FrameAutoShape
from ...frames.tools.framemovecenter import FrameMoveCenter
from ...frames.tools.framereplace import FrameReplace
from ...frames.tools.framemirror import FrameMirror
from ...frames.tools.framemiscellaneous import FrameMiscellaneous


class FrameTool(tk.Frame):
    """
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)  # , text="Tools"

        some_frame = tk.Frame(self)
        self.auto_shape = FrameAutoShape(some_frame)
        self.auto_shape.pack(side=tk.TOP, fill=tk.X, pady=2, padx=2)

        self.tool_mirror = FrameMirror(some_frame)
        self.tool_mirror.pack(side=tk.TOP, pady=10)
        some_frame.pack(side=tk.LEFT, fill=tk.Y, pady=5, padx=3)

        some_frame = tk.Frame(self)
        self.tool_move_center = FrameMoveCenter(some_frame)
        self.tool_move_center.pack(side=tk.TOP, pady=2, padx=2)

        self.tool_else = FrameMiscellaneous(some_frame)
        self.tool_else.pack(side=tk.TOP, fill=tk.X, pady=85, padx=2)
        some_frame.pack(side=tk.LEFT, fill=tk.Y, pady=5, padx=3)

        self.tool_replace = FrameReplace(self)
        self.tool_replace.pack(side=tk.TOP, pady=7, padx=3)
