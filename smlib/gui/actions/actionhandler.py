__author__ = 'Peter Hofmann'

from .actioncomponents import ActionComponents
from .actionautoshape import ActionAutoshape
from .actionmirror import ActionMirror
from .actionmiscellaneous import ActionMiscellaneous
from .actionmovecenter import ActionMoveCenter
from .actionreplace import ActionReplace
from .actionmenubar import ActionMenuBar


class ActionHandler(ActionComponents, ActionAutoshape, ActionMirror, ActionMiscellaneous, ActionMoveCenter, ActionReplace, ActionMenuBar):
    def __init__(self, main_frame, smbedit):
        """

        @type main_frame: smlib.gui.frames.mainframe.MainFrame
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        ActionComponents.__init__(self, main_frame, smbedit)
        ActionAutoshape.__init__(self, main_frame, smbedit)
        ActionMirror.__init__(self, main_frame, smbedit)
        ActionMiscellaneous.__init__(self, main_frame, smbedit)
        ActionMoveCenter.__init__(self, main_frame, smbedit)
        ActionReplace.__init__(self, main_frame, smbedit)
        ActionMenuBar.__init__(self, main_frame, smbedit)
