from PyQt5.QtWidgets import (QComboBox, QCheckBox, QVBoxLayout, QSplitter, QStatusBar,
                             QGridLayout, QHBoxLayout)
from PyQt5.QtGui import QTextCursor
from .tools.frametool import FrameTool
from .summary.framesummary import FrameSummary
from ..actions.actionmain import ActionMain
from ...utils.blockconfig import block_config


class MainFrame(ActionMain):
    """
    @type entities_combo_box: ttk.Combobox
    @type tool: FrameTool
    @type summary: FrameSummary
    @type menu_bar: smlib.gui.frames.menubar.MenuBar
    @type status_bar: QStatusBar
    @type entities_check_box: QCheckBox
    @type entities_combo_box: QComboBox
    """

    def __init__(self, status_bar, smbedit):
        super(MainFrame, self).__init__(smbedit)
        self.status_bar = status_bar
        self._current_index = 0
        self.list_of_entity_names = []

        self.tool = FrameTool(self, smbedit)
        self.summary = FrameSummary()
        # splitter1 = QSplitter(Qt.Horizontal)
        # splitter1.addWidget(self.tool)
        # splitter1.addWidget(self.summary)
        # splitter1.setHandleWidth(10)
        splitter1 = QHBoxLayout()
        splitter1.addWidget(self.tool)
        splitter1.addWidget(self.summary)

        v_box = QVBoxLayout()
        # v_box.addWidget(splitter1)
        v_box.addLayout(splitter1)
        self._gui_combobox_blueprint(v_box)
        self.setLayout(v_box)
        self.tool.tool_miscellaneous.refresh_combobox_values()
        self.disable()

    # #################
    # GUI
    # #################

    def _gui_combobox_blueprint(self, parent_box):
        """
        @type root_frame: MainFrame
        """
        self.entities_check_box = QCheckBox()
        self.entities_check_box.setText("Entity")

        self.entities_combo_box = QComboBox()
        self.entities_combo_box.setEditable(False)
        self.entities_combo_box.setStyleSheet("combobox-popup: 0;")
        self.entities_combo_box.setMaxVisibleItems(5)

        self.entities_check_box.stateChanged.connect(self.entities_check_box_onchange)
        self.entities_combo_box.currentIndexChanged.connect(self.entities_combo_box_onchange)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(0, 9)
        # grid.addWidget(label, 0, 0)
        grid.addWidget(self.entities_combo_box, 0, 0)
        grid.addWidget(self.entities_check_box, 0, 1)
        parent_box.addLayout(grid)

    def update_summary(self):
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        if len(self.list_of_entity_names) == 0:
            return
        self.summary.text_box.clear()

        self.update_header()
        self.update_logic()
        self.update_metadata()
        self.update_smd()
        self.summary.text_box.moveCursor(QTextCursor.Start)
        self.summary.text_box.ensureCursorVisible()

    def update_header(self):
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        current_index = self.entities_combo_box.currentIndex()
        self.summary.text_box.append("# Header v{}".format(
            self._smbedit.blueprint[current_index].header.version))
        self.summary.text_box.append("  Type: {}".format(
            self._smbedit.blueprint[current_index].header.get_type_name()))
        self.summary.text_box.append("  Role: {}".format(
            self._smbedit.blueprint[current_index].header.get_classification_name()))
        self.summary.text_box.append("  Width: {}".format(
            round(self._smbedit.blueprint[current_index].header.get_width())))
        self.summary.text_box.append("  Height: {}".format(
            round(self._smbedit.blueprint[current_index].header.get_height())))
        self.summary.text_box.append("  Length: {}".format(
            round(self._smbedit.blueprint[current_index].header.get_length())))

        self.summary.text_box.append("")

    def update_logic(self):
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        controller_version = 0
        current_index = self.entities_combo_box.currentIndex()
        tmp = self._smbedit.blueprint[current_index].logic._controller_version
        if tmp < -1:
            controller_version = abs(tmp) - 1024

        self.summary.text_box.append("# Logic v{}.{}".format(
            self._smbedit.blueprint[current_index].logic.version,
            controller_version
            ))
        self.summary.text_box.append("  Controllers: {}".format(
            len(self._smbedit.blueprint[current_index].logic._controller_position_to_block_id_to_block_positions)))

        self.summary.text_box.append("")

    def update_metadata(self):
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        current_index = self.entities_combo_box.currentIndex()
        self.summary.text_box.append("# Metadata v{}".format(
            self._smbedit.blueprint[current_index].meta._version))

        self.summary.text_box.append("")

    def update_smd(self):
        """
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        self.summary.text_box.append("# SMD")
        # self.summary.text_box.append("\tNumber of Blocks: ")
        if self.entities_check_box.checkState():
            current_index = self.entities_combo_box.currentIndex()
            self.summary.text_box.append("  Number of Blocks: {}".format(
                self._smbedit.blueprint[current_index].smd3.get_number_of_blocks()))
            block_id_to_quantity = self._smbedit.blueprint[current_index].smd3.get_block_id_to_quantity()
        else:
            total_sum = 0
            block_id_to_quantity = {}
            for blueprint in self._smbedit.blueprint:
                total_sum += blueprint.smd3.get_number_of_blocks()
                for block_id, quantity in blueprint.smd3.get_block_id_to_quantity().items():
                    if block_id not in block_id_to_quantity:
                        block_id_to_quantity[block_id] = 0
                    block_id_to_quantity[block_id] += quantity
            self.summary.text_box.append("  Number of Blocks: {}".format(total_sum))

        self.summary.text_box.append("")

        for block_id, quantity in block_id_to_quantity.items():
            self.summary.text_box.append("  {}: {}".format(str(quantity).rjust(6), block_config[block_id].name))

        self.summary.text_box.append("")

    def disable(self):
        self.entities_combo_box.setEnabled(False)
        self.entities_check_box.setEnabled(False)
        # self.summary.disable()
        self.tool.disable()

    def enable(self):
        self.entities_combo_box.setEnabled(True)
        self.entities_check_box.setEnabled(True)
        self.summary.enable()
        self.tool.enable()
