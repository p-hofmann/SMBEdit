__author__ = 'Peter Hofmann'

from smlib.gui.actions.actionautoshape import ActionAutoshape
from smlib.gui.actions.actionmirror import ActionMirror
from smlib.gui.actions.actionmiscellaneous import ActionMiscellaneous
from smlib.gui.actions.actionmovecenter import ActionMoveCenter
from smlib.gui.actions.actionreplace import ActionReplace
from smlib.gui.actions.actionmenubar import ActionMenuBar


class ActionHandler(ActionAutoshape, ActionMirror, ActionMiscellaneous, ActionMoveCenter, ActionReplace, ActionMenuBar):
    def __init__(self, main_frame, smbedit):
        """

        @type smbedit: SMBEdit
        """
        ActionAutoshape.__init__(self, main_frame, smbedit)
        ActionMirror.__init__(self, main_frame, smbedit)
        ActionMiscellaneous.__init__(self, main_frame, smbedit)
        ActionMoveCenter.__init__(self, main_frame, smbedit)
        ActionReplace.__init__(self, main_frame, smbedit)
        ActionMenuBar.__init__(self, main_frame, smbedit)
