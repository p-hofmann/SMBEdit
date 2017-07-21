__author__ = 'Peter Hofmann'


class ActionDefault(object):
    """
    Action class prototype

    @type _main_frame: smlib.gui.frames.mainframe.MainFrame
    @type _smbedit: smbeditGUI.SMBEditGUI
    """
    def __init__(self, main_frame, smbedit):
        """

        @type main_frame: smlib.gui.frames.mainframe.MainFrame
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        self._smbedit = smbedit
        self._main_frame = main_frame

    def set_commands(self):
        """
        Set commands of components
        """
        pass
