from PyQt5.QtWidgets import (QGridLayout, QPushButton, QVBoxLayout)
from ...actions.actionautoshape import ActionAutoshape


class FrameAutoShape(ActionAutoshape):
    """
    @type _main_frame: smlib.gui.frames.mainframe.MainFrame
    """

    def __init__(self, main_frame, smbedit):
        """
        """
        super(FrameAutoShape, self).__init__(main_frame, smbedit)
        self.setTitle("Autoshape")

        self.button_reset = QPushButton()
        self.button_reset.setText("Reset")

        self.button_wedge = QPushButton()
        self.button_wedge.setText("Wedge")

        self.button_tetra = QPushButton()
        self.button_tetra.setText("Tetra")

        self.button_corner = QPushButton()
        self.button_corner.setText("Corner")

        self.button_hepta = QPushButton()
        self.button_hepta.setText("Hepta")

        self.button_reset.clicked.connect(self.button_press_autoshape_reset)
        self.button_wedge.clicked.connect(self.button_press_autoshape_wedge)
        self.button_corner.clicked.connect(self.button_press_autoshape_corner)
        self.button_hepta.clicked.connect(self.button_press_autoshape_hepta)
        self.button_tetra.clicked.connect(self.button_press_autoshape_tetra)

        v_box = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(self.button_reset, 0, 0, 1, 2)
        grid.addWidget(self.button_wedge, 1, 0)
        grid.addWidget(self.button_tetra, 1, 1)
        grid.addWidget(self.button_corner, 2, 0)
        grid.addWidget(self.button_hepta, 2, 1)
        v_box.addLayout(grid)
        v_box.addStretch()

        self.setLayout(v_box)

    def disable(self):
        self.button_reset.setEnabled(False)
        self.button_wedge.setEnabled(False)
        self.button_tetra.setEnabled(False)
        self.button_corner.setEnabled(False)
        self.button_hepta.setEnabled(False)

    def enable(self):
        self.button_reset.setEnabled(True)
        self.button_wedge.setEnabled(True)
        self.button_tetra.setEnabled(True)
        self.button_corner.setEnabled(True)
        self.button_hepta.setEnabled(True)
