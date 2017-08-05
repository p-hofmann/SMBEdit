from PyQt5.QtWidgets import (QCompleter, QLabel, QGridLayout, QGroupBox, QComboBox, QSpacerItem, QFormLayout, QButtonGroup,
                             QPushButton, QWidget, QVBoxLayout, QLineEdit, QFrame)
from PyQt5.QtGui import QIntValidator
from ...actions.actionmovecenter import ActionMoveCenter


class FrameMoveCenter(ActionMoveCenter):
    """
    @type button_block_id: QPushButton
    @type button_vector: QPushButton
    """

    def __init__(self, main_frame, smbedit):
        super(FrameMoveCenter, self).__init__(main_frame, smbedit)
        self.setTitle("Move Center")
        v_box = QVBoxLayout()
        self._gui_move_center_by_block_id(v_box)
        self._gui_move_center_by_vector(v_box)
        v_box.addStretch()
        self.setLayout(v_box)

        self.button_block_id.pressed.connect(self.button_press_block_id)
        self.button_vector.pressed.connect(self.button_press_vector)

    # #################
    # GUI
    # #################

    def _gui_move_center_by_block_id(self, box):
        self.button_block_id = QPushButton()
        self.button_block_id.setText("Move to")
        self.button_block_id.setToolTip("Move to a specific block")
        # self.button_block_id.setMaximumWidth(20)

        self.block_id_combobox = QComboBox()
        self.block_id_combobox.setStyleSheet("combobox-popup: 0;")
        self.block_id_combobox.setMaxVisibleItems(10)
        # self.block_id_combobox.setEditable(True)
        # Widgets.insert_items(self.block_id_combobox)

        target_ids = {
            123: "Build Block",
            94: "Undeathinator",
            347: "Shop Module",
            56: "Gravity Unit",
            }
        for block_id, name in target_ids.items():
            self.block_id_combobox.addItem(name, block_id)
        # self.block_id_combobox.completer().setCompletionMode(QCompleter.PopupCompletion)

        grid = QGridLayout()
        grid.addWidget(self.block_id_combobox, 0, 0)
        grid.addWidget(self.button_block_id, 1, 0)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        grid.addWidget(line)

        box.addLayout(grid)

    def _gui_move_center_by_vector(self, box):
        self.variable_x = QLineEdit()
        self.variable_y = QLineEdit()
        self.variable_z = QLineEdit()
        self.variable_x.setText('0')
        self.variable_y.setText('0')
        self.variable_z.setText('0')
        self.variable_x.setValidator(QIntValidator())
        self.variable_y.setValidator(QIntValidator())
        self.variable_z.setValidator(QIntValidator())

        self.button_vector = QPushButton()
        self.button_vector.setText("Move by")
        self.button_vector.setToolTip("Move in a direction")

        grid = QGridLayout()
        grid.addWidget(QLabel("Right"), 0, 0)
        grid.addWidget(QLabel("Up"), 0, 1)
        grid.addWidget(QLabel("Forward"), 0, 2)
        grid.addWidget(self.variable_x, 1, 0)
        grid.addWidget(self.variable_y, 1, 1)
        grid.addWidget(self.variable_z, 1, 2)
        grid.addWidget(self.button_vector, 2, 0, 1, 3)

        box.addLayout(grid)

    def disable(self):
        self.button_block_id.setEnabled(False)
        self.button_vector.setEnabled(False)

    def enable(self):
        self.button_block_id.setEnabled(True)
        self.button_vector.setEnabled(True)
