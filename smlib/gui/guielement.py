__author__ = 'Peter Hofmann'

from .actions.actionautoshape import ActionAutoshape
from .actions.actionmirror import ActionMirror
from .actions.actionmiscellaneous import ActionMiscellaneous
from .actions.actionmovecenter import ActionMoveCenter
from .actions.actionreplace import ActionReplace
from .actions.actionmenubar import ActionMenuBar


class GuiElement(ActionAutoshape, ActionMirror, ActionMiscellaneous, ActionMoveCenter, ActionReplace, ActionMenuBar):
    def __init__(self, root, smbedit):
        """

        @type smbedit: SMBEdit
        """
        super(GuiElement, self).__init__(root, smbedit)
