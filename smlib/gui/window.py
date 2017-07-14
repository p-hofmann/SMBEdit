__author__ = 'Peter Hofmann'

import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk
from smlib.gui import GuiElement
# from smbeditGUI import SMBEditGUI


class Window(tk.Tk):
    def __init__(self, smbedit):
        """

        @type smbedit: SMBEditGUI
        """
        tk.Tk.__init__(self)
        self.root = GuiElement(self, smbedit)
