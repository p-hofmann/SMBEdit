from PyQt5.QtWidgets import (QSizePolicy, QSlider, QFormLayout, QGridLayout, QGroupBox, QListWidget, QWidget,
                             QStackedWidget, QScrollBar, QFormLayout, QAbstractScrollArea, QSpacerItem)
from PyQt5.QtCore import Qt
from .framemiscellaneous import FrameMiscellaneous
from .frameautoshape import FrameAutoShape
from .framemovecenter import FrameMoveCenter
from .framemirror import FrameMirror
from .framereplace import FrameReplace


class FrameTool(QGroupBox):
    """
    """

    def __init__(self, main_frame, smbedit):
        super().__init__('Tools')
        # self.tool_list = QListWidget()
        # self.tool_list.insertItem(0, 'Autoshape')
        # self.tool_list.insertItem(1, 'Move Center')
        # self.tool_list.insertItem(2, 'Mirror')
        # self.tool_list.insertItem(3, 'Remove/Replace')
        # self.tool_list.insertItem(4, 'Miscellaneous')
        # self.tool_list.setFixedSize(
        #     self.tool_list.sizeHintForColumn(0) + 2 * self.tool_list.frameWidth(),
        #     self.tool_list.sizeHintForRow(0) * self.tool_list.count() + 2 * self.tool_list.frameWidth())

        self.sp = QScrollBar(Qt.Horizontal)
        self.sp.setMaximum(4)
        self.sp.setToolTip("Slide between tool pages")
        self.sp.valueChanged[int].connect(self.value_change)

        self.tool_auto_shape = FrameAutoShape(main_frame, smbedit)
        self.tool_move_center = FrameMoveCenter(main_frame, smbedit)
        self.tool_mirror = FrameMirror(main_frame, smbedit)
        self.tool_replace = FrameReplace(main_frame, smbedit)
        self.tool_miscellaneous = FrameMiscellaneous(main_frame, smbedit)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.tool_auto_shape)
        self.stack.addWidget(self.tool_move_center)
        self.stack.addWidget(self.tool_mirror)
        self.stack.addWidget(self.tool_replace)
        self.stack.addWidget(self.tool_miscellaneous)

        grid = QGridLayout()
        # grid.addWidget(self.tool_list)
        # line = QFrame()
        # line.setFrameShape(QFrame.HLine)
        # grid.addWidget(line)
        grid.addWidget(self.sp)
        grid.addWidget(self.stack)
        self.setLayout(grid)
        # self.tool_list.currentRowChanged.connect(self.display)
        self.setMaximumWidth(250)

    def display(self, i):
        self.stack.setCurrentIndex(i)

    def value_change(self):
        self.stack.setCurrentIndex(self.sp.sliderPosition())

    def disable(self):
        self.tool_auto_shape.disable()
        self.tool_mirror.disable()
        self.tool_move_center.disable()
        self.tool_miscellaneous.disable()
        self.tool_replace.disable()

    def enable(self):
        self.tool_auto_shape.enable()
        self.tool_mirror.enable()
        self.tool_move_center.enable()
        self.tool_miscellaneous.enable()
        self.tool_replace.enable()
