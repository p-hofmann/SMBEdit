__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk
from ...frames.tools.frameautoshape import FrameAutoShape
from ...frames.tools.framemovecenter import FrameMoveCenter
from ...frames.tools.framereplace import FrameReplace
from ...frames.tools.framemirror import FrameMirror
from ...frames.tools.framemiscellaneous import FrameMiscellaneous


class FrameTool(tk.LabelFrame):
    """
    """

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text="Tools")

        note = ttk.Notebook(self)
        note.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, pady=2)

        some_frame = tk.Frame(note)
        self.auto_shape = FrameAutoShape(some_frame)
        self.auto_shape.pack(side=tk.TOP, fill=tk.X, pady=2, padx=2)

        self.tool_move_center = FrameMoveCenter(some_frame)
        self.tool_move_center.pack(side=tk.TOP, fill=tk.X, pady=2, padx=2)

        self.tool_mirror = FrameMirror(some_frame)
        self.tool_mirror.pack(side=tk.TOP, fill=tk.X, pady=2, padx=2)
        some_frame.pack(side=tk.LEFT, fill=tk.Y, pady=5, padx=3)
        note.add(some_frame, text="Shape")
        # note.add(some_frame, text="AutoShape/Mirror")

        self.tool_replace = FrameReplace(note)
        self.tool_replace.pack(side=tk.TOP, pady=7, padx=3)
        note.add(self.tool_replace, text="Replace")
        # note.add(self.tool_replace, text="Remove/Replace")

        some_frame = tk.Frame(note)
        self.tool_else = FrameMiscellaneous(some_frame)
        self.tool_else.pack(side=tk.TOP, fill=tk.X, pady=2, padx=2)
        some_frame.pack(side=tk.LEFT, fill=tk.Y, pady=5, padx=3)
        note.add(some_frame, text="Miscellaneous")
        # note.add(some_frame, text="MoveCenter/Miscellaneous")

    def disable(self):
        self.auto_shape.disable()
        self.tool_mirror.disable()
        self.tool_move_center.disable()
        self.tool_else.disable()
        self.tool_replace.disable()

    def enable(self):
        self.auto_shape.enable()
        self.tool_mirror.enable()
        self.tool_move_center.enable()
        self.tool_else.enable()
        self.tool_replace.enable()
