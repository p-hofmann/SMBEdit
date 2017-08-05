from PyQt5.QtWidgets import QAction, QMenu
from ..actions.actionmenubar import ActionMenuBar


class MenuBar(ActionMenuBar):

    def __init__(self, window, main_frame, smbedit):
        """

        @type window: smlib.gui.window.Window
        """
        super(MenuBar, self).__init__(window, main_frame, smbedit)
        menu_bar = window.menuBar()
        menu_file = menu_bar.addMenu('File')

        # menu_file_new = QAction('New', window)

        # import 3D model
        self.menu_file_import_3d_model = QAction('Import ...', window)

        # Load blueprint
        menu_file_load = QMenu('Load', window)
        self.menu_file_load_sment = QAction('Load .sment', window)
        self.menu_file_load_blueprint = QAction('Load blueprint', window)
        menu_file_load.addAction(self.menu_file_load_blueprint)
        menu_file_load.addAction(self.menu_file_load_sment)

        # Save blueprint
        menu_file_save = QMenu('Save', window)
        self.menu_file_save_sment = QAction('Save .sment', window)
        self.menu_file_save_blueprint = QAction('Save blueprint', window)
        menu_file_save.addAction(self.menu_file_save_blueprint)
        menu_file_save.addAction(self.menu_file_save_sment)

        menu_file.addMenu(menu_file_load)
        menu_file.addMenu(menu_file_save)
        menu_file.addSeparator()
        menu_file.addAction(self.menu_file_import_3d_model)

        # Tools
        menu_tools = menu_bar.addMenu('Tools')
        self.menu_tools_autoshape = QAction('Autoshape', window)
        self.menu_tools_move = QAction('Move Center', window)
        self.menu_tools_mirror = QAction('Mirror', window)
        self.menu_tools_replace = QAction('Remove/Replace', window)
        self.menu_tools_misc = QAction('Miscellaneous', window)

        menu_tools.addAction(self.menu_tools_autoshape)
        menu_tools.addAction(self.menu_tools_move)
        menu_tools.addAction(self.menu_tools_mirror)
        menu_tools.addAction(self.menu_tools_replace)
        menu_tools.addAction(self.menu_tools_misc)

        self.menu_tools_autoshape.setShortcut('Alt+1')
        self.menu_tools_move.setShortcut('Alt+2')
        self.menu_tools_mirror.setShortcut('Alt+3')
        self.menu_tools_replace.setShortcut('Alt+4')
        self.menu_tools_misc.setShortcut('Alt+5')

        # Settings
        menu_settings = menu_bar.addMenu('Settings')
        self.menu_settings_starmade_dir = QAction('Select StarMade folder', window)
        menu_settings.addAction(self.menu_settings_starmade_dir)

        #
        # menu_help = menu_bar.addMenu('Help')

        self.menu_file_exit = QAction('Exit', window)
        self.menu_file_exit.setShortcut('Ctrl+Q')
        self.menu_file_exit.setStatusTip('Exit application')
        self.menu_file_exit.triggered.connect(window.close)
        menu_file.addSeparator()
        menu_file.addAction(self.menu_file_exit)

        self.menu_file_import_3d_model.triggered.connect(self._dialog_file_import)
        self.menu_file_load_sment.triggered.connect(self._dialog_file_load)
        self.menu_file_load_blueprint.triggered.connect(self._dialog_directory_load)
        self.menu_file_save_sment.triggered.connect(self._dialog_file_save)
        self.menu_file_save_blueprint.triggered.connect(self._dialog_directory_save)
        self.menu_tools_autoshape.triggered.connect(lambda: self._main_frame.tool.display(0))
        self.menu_tools_move.triggered.connect(lambda: self._main_frame.tool.display(1))
        self.menu_tools_mirror.triggered.connect(lambda: self._main_frame.tool.display(2))
        self.menu_tools_replace.triggered.connect(lambda: self._main_frame.tool.display(3))
        self.menu_tools_misc.triggered.connect(lambda: self._main_frame.tool.display(4))
        self.menu_settings_starmade_dir.triggered.connect(self._dialog_directory_starmade)
