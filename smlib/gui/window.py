from .frames.mainframe import MainFrame
from .frames.menubar import MenuBar
from PyQt5.QtWidgets import QMainWindow


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
        self.setGeometry(150, 150, 550, 500)
        self.status_bar.showMessage('Ready')
