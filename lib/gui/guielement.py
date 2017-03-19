__author__ = 'Peter Hofmann'

from lib.gui.actions.actionautoshape import ActionAutoshape
from lib.gui.actions.actionmirror import ActionMirror
from lib.gui.actions.actionmiscellaneous import ActionMiscellaneous
from lib.gui.actions.actionmovecenter import ActionMoveCenter
from lib.gui.actions.actionreplace import ActionReplace
from lib.gui.actions.actionmenubar import ActionMenuBar


class GuiElement(ActionAutoshape, ActionMirror, ActionMiscellaneous, ActionMoveCenter, ActionReplace, ActionMenuBar):
    def __init__(self, root, smbedit):
        """

        @type smbedit: SMBEdit
        """
        super(GuiElement, self).__init__(root, smbedit)
