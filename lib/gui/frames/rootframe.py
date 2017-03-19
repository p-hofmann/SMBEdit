__author__ = 'Peter Hofmann'

import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk
from lib.gui.frames.menubar import MenuBar
from lib.gui.frames.mainframe import MainFrame
from lib.gui.frames.statusbar import StatusBar


class RootFrame(tk.Frame):
    def __init__(self, root, smbedit):
        """

        @type root: tk.Tk
        """
        tk.Frame.__init__(self, root)
        self.menubar = MenuBar(root)

        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill=tk.BOTH, padx=5, pady=3)

        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.set("Ready")

        self.pack()
