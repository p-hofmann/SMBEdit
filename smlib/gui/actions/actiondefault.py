from PyQt5.QtWidgets import QWidget, QGroupBox


class ActionDefault(QGroupBox):
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
        super().__init__()
        self._smbedit = smbedit
        self._main_frame = main_frame
