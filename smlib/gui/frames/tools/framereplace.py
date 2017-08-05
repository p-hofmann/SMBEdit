from PyQt5.QtWidgets import (QLabel, QGridLayout, QGroupBox, QComboBox, QSpacerItem, QFormLayout,
                             QPushButton, QVBoxLayout, QFrame)
from ...frames.widgets import Widgets
from ...actions.actionreplace import ActionReplace


class FrameReplace(ActionReplace):
    """
    """

    def __init__(self, main_frame, smbedit):
        super(FrameReplace, self).__init__(main_frame, smbedit)
        self.setTitle("Remove/Replace")

        v_box = QVBoxLayout()
        self._gui_remove_block(v_box)
        self._gui_replace_block(v_box)
        self._gui_replace_hull_and_armor(v_box)
        v_box.addStretch()
        self.setLayout(v_box)

        self.button_remove.pressed.connect(self.button_press_remove)
        self.button_replace_block.pressed.connect(self.button_press_replace_block)
        self.button_replace_hull.pressed.connect(self.button_press_replace_hull)

    # #################
    # GUI
    # #################

    def _gui_remove_block(self, box):
        # TOP
        self.combobox_remove_blocks = QComboBox()
        self.combobox_remove_blocks.setEditable(True)
        self.combobox_remove_blocks.setStyleSheet("combobox-popup: 0;")
        self.combobox_remove_blocks.setMaxVisibleItems(10)
        Widgets.insert_items(self.combobox_remove_blocks)
        self.button_remove = QPushButton("Remove block type")

        grid = QGridLayout()
        grid.addWidget(self.combobox_remove_blocks)
        grid.addWidget(self.button_remove)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        grid.addWidget(line)
        box.addLayout(grid)
        # combobox.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
        # TOP END

    def _gui_replace_block(self, box):
        # combobox->findText("level"); // prints - 1, not found

        self.combobox_replace_original = QComboBox()
        self.combobox_replace_original.setEditable(True)
        self.combobox_replace_original.setStyleSheet("combobox-popup: 0;")
        self.combobox_replace_original.setMaxVisibleItems(10)
        Widgets.insert_items(self.combobox_replace_original)

        self.combobox_replace_replacement = QComboBox()
        self.combobox_replace_replacement.setEditable(True)
        self.combobox_replace_replacement.setStyleSheet("combobox-popup: 0;")
        self.combobox_replace_replacement.setMaxVisibleItems(10)
        Widgets.insert_items(self.combobox_replace_replacement)

        self.button_replace_block = QPushButton("Replace block type")

        grid = QGridLayout()
        grid.addWidget(self.combobox_replace_original)
        grid.addWidget(self.combobox_replace_replacement)
        grid.addWidget(self.button_replace_block)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        grid.addWidget(line)
        box.addLayout(grid)

    def _gui_replace_hull_and_armor(self, box):
        tiers = ["Hull", "Std. armor", "Adv. armor", "Crystal armor", "Hazard armor"]
        self.combobox_replace_hull_original = QComboBox()
        # self.combobox_replace_hull_original.setEditable(True)
        self.combobox_replace_hull_original.setStyleSheet("combobox-popup: 0;")
        self.combobox_replace_hull_original.setMaxVisibleItems(10)

        self.combobox_replace_hull_replacement = QComboBox()
        # self.combobox_replace_hull_replacement.setEditable(True)
        self.combobox_replace_hull_replacement.setStyleSheet("combobox-popup: 0;")
        self.combobox_replace_hull_replacement.setMaxVisibleItems(10)
        for index, tier in enumerate(tiers):
            self.combobox_replace_hull_original.addItem(tier)
            if index > 2:
                continue
            self.combobox_replace_hull_replacement.addItem(tier)
        self.combobox_replace_hull_original.addItem("All")

        self.button_replace_hull = QPushButton("Replace")

        # label = QLabel("To")
        form = QFormLayout()
        form.addRow(QLabel("From"), self.combobox_replace_hull_original)
        form.addRow(QLabel("To"), self.combobox_replace_hull_replacement)
        box.addLayout(form)
        box.addWidget(self.button_replace_hull)

    def disable(self):
        self.button_remove.setEnabled(False)
        self.button_replace_hull.setEnabled(False)
        self.button_replace_block.setEnabled(False)

    def enable(self):
        self.button_remove.setEnabled(True)
        self.button_replace_hull.setEnabled(True)
        self.button_replace_block.setEnabled(True)
