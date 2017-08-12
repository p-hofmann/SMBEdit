from .frames.mainframe import MainFrame
from .frames.menubar import MenuBar
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QProgressBar


class Window(QMainWindow):
    """
    @type status_bar: QStatusBar
    """
    def __init__(self, smbedit):
        """

        @type smbedit: SMBEditGUI
        """
        super().__init__()

        # ################
        # Status Bar
        # ################
        self.status_bar = self.statusBar()
        self.progressBar = QProgressBar()
        # self.status_bar.add(self.progressBar)
        self.status_bar.addPermanentWidget(self.progressBar)
        self.progressBar.setMaximumWidth(200)
        self.progressBar.setMaximumHeight(20)
        self.progressBar.setHidden(True)

        main_frame = MainFrame(self.status_bar, smbedit)
        self.setCentralWidget(main_frame)

        # ################
        # Menu Bar
        # ################
        self.menu_bar = MenuBar(self, main_frame, smbedit)

        #                  x    y    w    h
        self.setGeometry(150, 150, 550, 500)
        self.status_bar.showMessage('Ready')

    def print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=20, fill='X'):
        """
        Original:
            https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        # percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        percent = int(100 * (iteration / float(total)))
        # filled_length = int(length * iteration // total)
        # bar = fill * filled_length + '+' * (length - filled_length)
        # self.status_bar.showMessage('%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
        self.progressBar.setValue(percent)
