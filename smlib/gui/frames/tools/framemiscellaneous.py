from PyQt5.QtWidgets import QLabel, QVBoxLayout, QGroupBox, QComboBox, QPushButton, QFormLayout
from ....utils.blueprintentity import BlueprintEntity
from ...actions.actionmiscellaneous import ActionMiscellaneous


class FrameMiscellaneous(ActionMiscellaneous):
    """
    @type combo_box_type: QComboBox
    @type combo_box_class: QComboBox
    """

    def __init__(self, main_frame, smbedit):
        """
        """
        super().__init__(main_frame, smbedit)
        self.setTitle("Miscellaneous")
        # v_box = QVBoxLayout()
        # self._gui_entity_type(v_box)
        # v_box.addSpacerItem(QSpacerItem(100, 10))
        # self._gui_entity_class(v_box)
        # v_box.addStretch()
        # self.setLayout(v_box)

        my_form = QFormLayout()
        self._gui_entity_type(my_form)
        self._gui_entity_class(my_form)

        self.combo_box_type.currentIndexChanged.connect(self.combo_box_type_change)
        # self.combo_box_class.currentIndexChanged.connect(self.combo_box_class_change)

        self.confirm = QPushButton("Confirm")
        self.confirm.pressed.connect(self.on_click_confirm)

        v_box = QVBoxLayout()
        v_box.addLayout(my_form)
        v_box.addWidget(self.confirm)
        v_box.addStretch()

        self.setLayout(v_box)

    def _gui_entity_type(self, box):
        label = QLabel()
        label.setText("Type:")
        self.combo_box_type = QComboBox()
        self.combo_box_type.setEditable(False)
        self.combo_box_type.insertItems(0, list(BlueprintEntity.entity_types.values()))
        box.addRow(label, self.combo_box_type)
        # box.addWidget(label)
        # box.addWidget()

    def _gui_entity_class(self, box):
        label = QLabel()
        label.setText("Role:")
        self.combo_box_class = QComboBox()
        self.combo_box_class.setEditable(False)

        self.combo_box_class.insertItem(0, "General")
        box.addRow(label, self.combo_box_class)
        # box.addWidget(label)
        # box.addWidget(self.combo_box_class)

    def disable(self):
        # self.combo_box_type.setEnabled(False)
        # self.combo_box_class.setEnabled(False)
        self.confirm.setEnabled(False)

    def enable(self):
        # self.combo_box_type.setEnabled(True)
        # self.combo_box_class.setEnabled(True)
        self.confirm.setEnabled(True)
