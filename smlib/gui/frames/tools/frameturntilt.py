from PyQt5.QtWidgets import (QGridLayout, QPushButton, QVBoxLayout, QLabel)
from ...actions.actionturntilt import ActionTurnTilt


class FrameTurnTilt(ActionTurnTilt):
    """
    @type _main_frame: smlib.gui.frames.mainframe.MainFrame
    """

    def __init__(self, main_frame, smbedit):
        """
        0: # tilt up
        1: # tilt down
        2: # turn right
        3: # turn left
        4: # tilt right
        5: # tilt left
        """
        super(FrameTurnTilt, self).__init__(main_frame, smbedit)
        self.setTitle("Turn/Tilt")

        self.button_turn_left = QPushButton()
        self.button_turn_right = QPushButton()
        self.button_tilt_left = QPushButton()
        self.button_tilt_right = QPushButton()
        self.button_tilt_up = QPushButton()
        self.button_tilt_down = QPushButton()

        self.button_turn_left.setText("Turn Left")
        self.button_turn_right.setText("Turn Right")
        self.button_tilt_left.setText("Tilt Left")
        self.button_tilt_right.setText("Tilt Right")
        self.button_tilt_up.setText("Tilt Up")
        self.button_tilt_down.setText("Tilt Down")

        self.button_tilt_up.clicked.connect(lambda: self.button_press(0))
        self.button_tilt_down.clicked.connect(lambda: self.button_press(1))
        self.button_turn_right.clicked.connect(lambda: self.button_press(2))
        self.button_turn_left.clicked.connect(lambda: self.button_press(3))
        self.button_tilt_right.clicked.connect(lambda: self.button_press(4))
        self.button_tilt_left.clicked.connect(lambda: self.button_press(5))

        v_box = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(self.button_turn_left, 0, 0)
        grid.addWidget(self.button_tilt_up, 0, 1)
        grid.addWidget(self.button_turn_right, 0, 2)
        grid.addWidget(self.button_tilt_left, 1, 0)
        grid.addWidget(self.button_tilt_down, 1, 1)
        grid.addWidget(self.button_tilt_right, 1, 2)
        grid.addWidget(QLabel("Warning:"), 2, 0, 1, 3)
        grid.addWidget(QLabel("  Block faces are not turned."), 3, 0, 1, 3)
        grid.addWidget(QLabel("  Will break docking."), 4, 0, 1, 3)
        v_box.addLayout(grid)
        v_box.addStretch()

        self.setLayout(v_box)

    def disable(self):
        self.button_turn_left.setEnabled(False)
        self.button_turn_right.setEnabled(False)
        self.button_tilt_left.setEnabled(False)
        self.button_tilt_right.setEnabled(False)
        self.button_tilt_up.setEnabled(False)
        self.button_tilt_down.setEnabled(False)

    def enable(self):
        self.button_turn_left.setEnabled(True)
        self.button_turn_right.setEnabled(True)
        self.button_tilt_left.setEnabled(True)
        self.button_tilt_right.setEnabled(True)
        self.button_tilt_up.setEnabled(True)
        self.button_tilt_down.setEnabled(True)
