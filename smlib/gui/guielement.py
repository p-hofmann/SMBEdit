__author__ = 'Peter Hofmann'

from smlib.gui import ActionAutoshape
from smlib.gui import ActionMirror
from smlib.gui import ActionMiscellaneous
from smlib.gui import ActionMoveCenter
from smlib.gui import ActionReplace
from smlib.gui import ActionMenuBar


class GuiElement(ActionAutoshape, ActionMirror, ActionMiscellaneous, ActionMoveCenter, ActionReplace, ActionMenuBar):
    def __init__(self, root, smbedit):
        """

        @type smbedit: SMBEdit
        """
        super(GuiElement, self).__init__(root, smbedit)
