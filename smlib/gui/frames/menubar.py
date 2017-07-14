__author__ = 'Peter Hofmann'

import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk


class MenuBar(tk.Menu):

    def __init__(self, root):
        """

        @type root: tk.Tk
        @return:
        """
        tk.Menu.__init__(self, root)
        root.config(menu=self)
        self.menu_cascade_load = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Load", menu=self.menu_cascade_load)
        self.menu_cascade_save = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Save", menu=self.menu_cascade_save)
