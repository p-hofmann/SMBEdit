__author__ = 'Peter Hofmann'

import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk
from smlib.gui.actions.actionhandler import ActionHandler
from .frames.mainframe import MainFrame


class Window(tk.Tk):
    def __init__(self, smbedit):
        """

        @type smbedit: SMBEditGUI
        """
        tk.Tk.__init__(self)
        self.main_frame = MainFrame(self)
        self.actionhandler = ActionHandler(self.main_frame, smbedit)
