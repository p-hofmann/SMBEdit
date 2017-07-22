__author__ = 'Peter Hofmann'

import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk
from .frames.mainframe import MainFrame
from .actions.actionmain import ActionMain
from .actions.actionautoshape import ActionAutoshape
from .actions.actionmirror import ActionMirror
from .actions.actionmiscellaneous import ActionMiscellaneous
from .actions.actionmovecenter import ActionMoveCenter
from .actions.actionreplace import ActionReplace
from .actions.actionmenubar import ActionMenuBar


class Window(tk.Tk, ActionMain, ActionAutoshape, ActionMirror, ActionMiscellaneous, ActionMoveCenter, ActionReplace, ActionMenuBar):
    def __init__(self, smbedit):
        """

        @type smbedit: SMBEditGUI
        """
        tk.Tk.__init__(self)
        main_frame = MainFrame(self)

        ActionMain.__init__(self, main_frame, smbedit)
        # ActionAutoshape.__init__(self, main_frame, smbedit)
        # ActionMirror.__init__(self, main_frame, smbedit)
        # ActionMiscellaneous.__init__(self, main_frame, smbedit)
        # ActionMoveCenter.__init__(self, main_frame, smbedit)
        # ActionReplace.__init__(self, main_frame, smbedit)
        # ActionMenuBar.__init__(self, main_frame, smbedit)
