from PyQt5.QtWidgets import QTextEdit, QGroupBox, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont


class FrameSummary(QGroupBox):
    """
    @type text_box: StreamToTkText
    """

    def __init__(self):
        super().__init__('Summary')
        # title = QLabel()
        # self.addWidget(title)

        v_box = QVBoxLayout()
        self.text_box = QTextEdit()
        font = QFont("Courier")
        font.setPointSize(10)
        self.text_box.setCurrentFont(font)
        self.text_box.setLineWrapMode(QTextEdit.NoWrap)
        v_box.addWidget(self.text_box)
        self.setLayout(v_box)

    def disable(self):
        pass

    def enable(self):
        pass
