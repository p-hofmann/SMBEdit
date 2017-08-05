from .frames.mainframe import MainFrame
from .frames.menubar import MenuBar
# from .actions.actionmain import ActionMain
# from .actions.actionautoshape import ActionAutoshape
# from .actions.actionmirror import ActionMirror
# from .actions.actionmiscellaneous import ActionMiscellaneous
# from .actions.actionmovecenter import ActionMoveCenter
# from .actions.actionreplace import ActionReplace
# from .actions.actionmenubar import ActionMenuBar
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QMenu


class Window(QMainWindow):
    def __init__(self, smbedit):
        """

        @type smbedit: SMBEditGUI
        """
        super().__init__()

        # ################
        # Status Bar
        # ################
        self.status_bar = self.statusBar()

        main_frame = MainFrame(self.status_bar, smbedit)
        self.setCentralWidget(main_frame)

        # ################
        # Menu Bar
        # ################
        self.menu_bar = MenuBar(self, main_frame, smbedit)

        #                  x    y    w    h
        self.setGeometry(300, 300, 550, 500)
        self.status_bar.showMessage('Ready')
