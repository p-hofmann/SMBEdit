from PyQt5.QtWidgets import (QSizePolicy, QFrame, QFormLayout, QGridLayout, QGroupBox, QCheckBox, QWidget,
                             QStackedWidget, QVBoxLayout, QPushButton, QRadioButton, QButtonGroup)
from ...actions.actionmirror import ActionMirror


class FrameMirror(ActionMirror):
    """
    """

    def __init__(self, main_frame, smbedit):
        """
        """
        super(FrameMirror, self).__init__(main_frame, smbedit)
        self.setTitle("Mirror")
        self._gui_mirror()

    def _gui_mirror(self):
        """
        0: x left to right
        1: y top to bottom
        2: z front to back
        """
        # TOP
        radio_box_option_x = QRadioButton("Left to Right")
        radio_box_option_y = QRadioButton("Top to Bottom")
        radio_box_option_z = QRadioButton("Front to Back")
        self.button_group = QButtonGroup()
        self.button_group.addButton(radio_box_option_x, 0)
        self.button_group.addButton(radio_box_option_y, 1)
        self.button_group.addButton(radio_box_option_z, 2)
        radio_box_option_x.setChecked(True)
        # TOP END

        # BOTTOM
        self.check_button = QCheckBox("Reverse")

        self.button_mirror = QPushButton("Mirror")
        self.button_mirror.pressed.connect(self.button_press_mirror)
        # BOTTOM END

        grid = QGridLayout()
        grid.addWidget(radio_box_option_x, 0, 0)
        grid.addWidget(radio_box_option_z, 1, 0)
        grid.addWidget(radio_box_option_y, 2, 0)
        grid.addWidget(self.check_button, 3, 0)
        grid.addWidget(self.button_mirror, 4, 0)

        v_box = QVBoxLayout()
        v_box.addLayout(grid)
        v_box.addStretch()
        self.setLayout(v_box)

    def disable(self):
        self.button_mirror.setEnabled(False)

    def enable(self):
        self.button_mirror.setEnabled(True)
