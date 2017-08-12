import os
import zipfile
import tempfile
from ...common.validator import Validator
from ...blueprint import Blueprint
from ...utils.blockconfig import block_config
from ...cli.edit import SMBEdit
from.actiondefault import ActionDefault
from voxlib.voxelize import voxelize
from PyQt5.QtWidgets import QFileDialog, QInputDialog


class ActionMenuBar(ActionDefault):
    """
    Dealing with component interactions

    @type _smbedit: smbeditGUI.SMBEditGUI
    """
    def __init__(self, window, main_frame, smbedit):
        """

        @type window: smlib.gui.window.Window
        @type main_frame: smlib.gui.frames.mainframe.MainFrame
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        super(ActionMenuBar, self).__init__(main_frame, smbedit)
        self._window = window

    _file_types = [
        ("Blueprint", "*.sment"),
        ("Blueprint", "*.zip")
        ]

    @staticmethod
    def get_resolution():
        value, confirmed = QInputDialog.getInt(None, "Model resolution", "Maximum resolution:", 100, 0, 5000, 1)
        if confirmed:
            return value
        return None

    def _dialog_file_import(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade and os.path.exists(self._smbedit.directory_starmade):
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.AnyFile
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            caption='Import file',
            directory=blueprint_dir,
            filter="3D model (*.obj *.stl);; obj Archive (*.zip);; All Files (*)",
            options=options
        )
        if not file_path:
            return

        resolution = self.get_resolution()
        if not resolution:
            return

        try:
            self._window.progressBar.setHidden(False)
            self._window.status_bar.showMessage("Voxelizing 3D model ...")
            voxel_positions = set(voxelize(file_path, resolution, self._window.print_progress_bar))
            self._window.status_bar.showMessage("Making StarMade blueprint ...")

            entity_name = 'Main'
            self.list_of_entity_names = [entity_name]
            self._smbedit._directory_input = ['']
            self._smbedit.blueprint = [Blueprint(entity_name, verbose=False, debug=False)]

            self._smbedit.blueprint[0].add_blocks(598, voxel_positions, offset=(16, 16, 16))
            self._smbedit.blueprint[0].add_blocks(1, [(16, 16, 16)])
            self._smbedit.blueprint[0].set_entity(0, 0)

            self._main_frame.entities_combo_box.clear()
            self._main_frame.entities_combo_box.addItem('All')
            self._main_frame.entities_check_box.setChecked(False)
            self._main_frame.update_summary()
            self._main_frame.enable()
            self._window.status_bar.showMessage("Import complete.")
        except AssertionError as e:
            self._window.progressBar.setHidden(True)
            self._main_frame.status_bar.showMessage("Error: {}".format(e))
        finally:
            self._window.progressBar.setHidden(True)

    # #################
    # Get Starmade directory
    # #################

    def _dialog_directory_starmade(self):
        starmade_dir = None
        if self._smbedit.directory_starmade and os.path.exists(self._smbedit.directory_starmade):
            starmade_dir = self._smbedit.directory_starmade

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        file_dialog = QFileDialog()
        directory_input = file_dialog.getExistingDirectory(
            caption="Select 'StarMade' folder",
            directory=starmade_dir,
            options=options)

        if not directory_input:
            return
        msg_input_invalid = "StarMade directory is invalid: '{}'".format(os.path.basename(directory_input))
        if not Validator().validate_dir(directory_input, file_names=["StarMade.jar"], silent=True):
            self._window.status_bar.showMessage("Error: {}".format(msg_input_invalid))
            return
        self._smbedit.directory_starmade = directory_input
        self._smbedit.save_starmade_directory(directory_input)
        block_config.read(directory_input)

    # #################
    # Load Save Dialog
    # #################

    def _dialog_file_load(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade and os.path.exists(self._smbedit.directory_starmade):
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.AnyFile
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            caption='Load file',
            directory=blueprint_dir,
            filter="Blueprint (*.sment *.zip);; All Files (*)",
            options=options
        )
        if not file_path:
            return
        if not zipfile.is_zipfile(file_path):
            self._window.status_bar.showMessage("Error: Not a zip compressed file.")
            return

        tmp_directory_input = tempfile.mkdtemp(dir=self._smbedit.tmp_dir)
        with zipfile.ZipFile(file_path, "r") as read_handler:
            read_handler.extractall(tmp_directory_input)
        list_of_dir = os.listdir(tmp_directory_input)
        if len(list_of_dir) != 1:
            self._window.status_bar.showMessage("Error: Invalid sment file content.")
            return
        blueprint_name = list_of_dir[0]
        directory_input = os.path.join(tmp_directory_input, blueprint_name)
        self.load_blueprint(directory_input)

    def _dialog_file_save(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade and os.path.exists(self._smbedit.directory_starmade):
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.AnyFile
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            caption='Save as ...',
            directory=blueprint_dir,
            filter="Blueprint (*.sment *.zip);; All Files (*)",
            options=options,
            )

        if not file_path:
            return
        if not os.path.splitext(file_path)[1]:
            # todo: find a way to do this with QFileDialog
            file_path += ".sment"
        if not Validator().validate_dir(file_path, only_parent=True):
            self._window.status_bar.showMessage("Error: Invalid directory.")
            return

        blueprint_name = os.path.splitext(os.path.basename(file_path))[0]
        directory_output = os.path.join(tempfile.mkdtemp(dir=self._smbedit.tmp_dir), blueprint_name)
        self.save_blueprint(directory_output)
        SMBEdit.zip_directory(directory_output, file_path)

    def _dialog_directory_load(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade and os.path.exists(self._smbedit.directory_starmade):
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        file_dialog = QFileDialog()
        directory_input = file_dialog.getExistingDirectory(
            caption='Load Blueprint',
            directory=blueprint_dir,
            options=options)

        if not directory_input:
            return
        file_names = ["header.smbph", "logic.smbpl", "meta.smbpm"]
        msg_input_invalid = "Blueprint input is invalid: '{}'".format(os.path.basename(directory_input))
        if not Validator().validate_dir(directory_input, file_names=file_names):
            self._window.status_bar.showMessage("Error: {}".format(msg_input_invalid))
            return
        directory_input = directory_input
        self.load_blueprint(directory_input)

    def _dialog_directory_save(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade and os.path.exists(self._smbedit.directory_starmade):
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        file_dialog = QFileDialog()
        directory_output = file_dialog.getExistingDirectory(
            caption='Save Blueprint',
            directory=blueprint_dir,
            options=options)

        if not directory_output:
            return
        msg_input_invalid = "Invalid Blueprint directory path: '{}'".format(directory_output)
        if not Validator().validate_dir(directory_output, only_parent=True):
            self._window.status_bar.showMessage("Error: {}".format(msg_input_invalid))
            return
        if os.path.exists(directory_output):
            if len(os.listdir(directory_output)) > 0:
                msg_input_invalid = "Output directory is not empty, aborting to prevent overwriting.".format(
                    directory_output)
                self._window.status_bar.showMessage("Error: {}".format(msg_input_invalid))
                return
        directory_output = directory_output
        self.save_blueprint(directory_output)

    # #################
    # Load Save
    # #################

    def save_blueprint(self, directory_output):
        directory_output = Validator.get_full_path(directory_output)
        blueprint_name = os.path.basename(directory_output)
        msg = "Saving blueprint '{}'... ".format(blueprint_name)
        self._window.status_bar.showMessage(msg)
        for index, blueprint in enumerate(self._smbedit.blueprint):
            relative_path = os.path.join(blueprint_name, self._smbedit._directory_input[index])
            blueprint_output = os.path.join(directory_output, self._smbedit._directory_input[index])
            if self._smbedit._directory_input[index] == '':
                relative_path = blueprint_name
                blueprint_output = directory_output
            self._window.status_bar.showMessage("Writing\t'{}'".format(relative_path))
            if not os.path.exists(blueprint_output):
                os.mkdir(blueprint_output)
            blueprint.write(blueprint_output, relative_path)
        self._main_frame.clear_blueprint()
        self._window.status_bar.showMessage(msg + " Done")

    def load_blueprint(self, directory_base):
        self._smbedit.blueprint = []
        self._smbedit._directory_input = []

        blueprint_name = os.path.basename(directory_base)
        msg = "Loading blueprint '{}'... ".format(blueprint_name)
        self._window.status_bar.showMessage(msg)
        directory_base = Validator.get_full_path(directory_base)
        index = 0
        is_docked_entity = False
        tmp_list_path = list()
        self._main_frame.list_of_entity_names = list()
        tmp_list_path.append(directory_base)
        self._main_frame.list_of_entity_names.append("MAIN")
        while index < len(tmp_list_path):
            blueprint_path = tmp_list_path[index]
            entity_name = self._main_frame.list_of_entity_names[index]
            relative_path = os.path.relpath(blueprint_path, directory_base)
            if relative_path == '.':
                relative_path = ''
            self._smbedit._directory_input.append(relative_path)
            if relative_path == '':
                relative_path = blueprint_name
            self._window.status_bar.showMessage("Reading:\t'{}' ...".format(os.path.join(blueprint_name, relative_path)))
            index += 1
            blueprint = Blueprint(entity_name, verbose=False, debug=False)
            blueprint.read(blueprint_path)
            docked_entity_name_prefix = "{}__ATTACHED_".format(entity_name)
            blueprint.replace_outdated_docker_modules(docked_entity_name_prefix, is_docked_entity)
            self._smbedit.blueprint.append(blueprint)
            is_docked_entity = True

            list_of_folders = os.listdir(blueprint_path)
            for folder_name in sorted(list_of_folders):
                if "ATTACHED_" not in folder_name:
                    continue
                new_path = os.path.join(blueprint_path, folder_name)
                if not os.path.isdir(new_path):
                    continue
                _, dock_index = folder_name.rsplit('_', 1)
                tmp_list_path.append(os.path.join(blueprint_path, folder_name))
                self._main_frame.list_of_entity_names.append("{}{}".format(docked_entity_name_prefix, dock_index))

        self._window.status_bar.showMessage(msg + " Done")
        self._main_frame.entities_combo_box.clear()
        self._main_frame.entities_combo_box.addItem('All')
        self._main_frame.entities_check_box.setChecked(False)
        self._main_frame.update_summary()
        self._main_frame.enable()
