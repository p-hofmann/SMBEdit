import os
import zipfile
import tempfile
from PyQt5.QtWidgets import QFileDialog
from smbedit import SMBEdit
from.actiondefault import ActionDefault
from ...common.validator import Validator
from ...blueprint import Blueprint
from ...utils.blockconfig import block_config


class ActionMenuBar(ActionDefault):
    """
    Dealing with component interactions
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

    def _dialog_directory_starmade(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade:
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        file_dialog = QFileDialog()
        # file_dialog.setFilter("Sment files (*.sment *.zip)")
        directory_input = file_dialog.getExistingDirectory(
            caption="Select 'StarMade' folder",
            directory=blueprint_dir,
            options=options)
        # print("Dir", directory_input)

        if not directory_input:
            return
        msg_input_invalid = "StarMade directory is invalid: '{}'".format(os.path.basename(directory_input))
        if not Validator().validate_dir(directory_input, file_names=["StarMade.jar"], silent=True):
            # messagebox.showwarning("Blueprint", msg_input_invalid)
            self._window.status_bar.showMessage("Error: {}".format(msg_input_invalid))
            return
        self._smbedit.directory_starmade = directory_input
        self._smbedit.save_starmade_directory(directory_input)
        block_config.read(directory_input)

    def _dialog_file_load(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade:
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.AnyFile
        # options |= QFileDialog.ExistingFile
        file_dialog = QFileDialog()
        # file_dialog.setNameFilter()
        file_path, _ = file_dialog.getOpenFileName(
            caption='Load file',
            directory=blueprint_dir,
            filter="Blueprint (*.sment *.zip);; All Files (*)",
            options=options
        )
        # filetypes=ActionMenuBar._file_types
        if not file_path:
            return
        # if not self.validate_file(file_path):
        #     return
        # if not self.validate_file(file_path, silent=True):
        #     messagebox.showwarning("Blueprint", "Invalid sment file.")
        #     return
        if not zipfile.is_zipfile(file_path):
            # messagebox = QMessageBox.warning()
            # messagebox.showwarning("Blueprint", "Not a zip compressed file.")
            self._window.status_bar.showMessage("Error: Not a zip compressed file.")
            return

        tmp_directory_input = tempfile.mkdtemp(dir=self._smbedit.tmp_dir)
        with zipfile.ZipFile(file_path, "r") as read_handler:
            read_handler.extractall(tmp_directory_input)
        list_of_dir = os.listdir(tmp_directory_input)
        if len(list_of_dir) != 1:
            # messagebox.showwarning("Blueprint", "Invalid sment file content.")
            self._window.status_bar.showMessage("Error: Invalid sment file content.")
            # QMessageBox.Ok
            return
        blueprint_name = list_of_dir[0]
        directory_input = os.path.join(tmp_directory_input, blueprint_name)
        self.load_blueprint(directory_input)

    def _dialog_file_save(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade:
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.AnyFile
        file_dialog = QFileDialog()
        # file_dialog.setDefaultSuffix("sment")
        # file_dialog.setFilter("Sment files (*.sment *.zip)")
        file_path, _ = file_dialog.getSaveFileName(
            caption='Save as ...',
            directory=blueprint_dir,
            filter="Blueprint (*.sment *.zip);; All Files (*)",
            options=options,
            )
        # print("SFile:", file_path)

        if not file_path:
            return
        if not os.path.splitext(file_path)[1]:
            # todo: find a way to do this with QFileDialog
            file_path += ".sment"
        if not Validator().validate_dir(file_path, only_parent=True):
            # messagebox.showwarning("Blueprint", "Invalid directory.")
            self._window.status_bar.showMessage("Error: Invalid directory.")
            return

        blueprint_name = os.path.splitext(os.path.basename(file_path))[0]
        directory_output = os.path.join(tempfile.mkdtemp(dir=self._smbedit.tmp_dir), blueprint_name)
        self.save_blueprint(directory_output)
        SMBEdit.zip_directory(directory_output, file_path)

    def _dialog_directory_load(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade:
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        file_dialog = QFileDialog()
        # file_dialog.setFilter("Sment files (*.sment *.zip)")
        directory_input = file_dialog.getExistingDirectory(
            caption='Load Blueprint',
            directory=blueprint_dir,
            options=options)
        # print("Dir", directory_input)

        if not directory_input:
            return
        file_names = ["header.smbph", "logic.smbpl", "meta.smbpm"]
        msg_input_invalid = "Blueprint input is invalid: '{}'".format(os.path.basename(directory_input))
        if not Validator().validate_dir(directory_input, file_names=file_names):
            # messagebox.showwarning("Blueprint", msg_input_invalid)
            self._window.status_bar.showMessage("Error: {}".format(msg_input_invalid))
            return
        directory_input = directory_input
        self.load_blueprint(directory_input)

    def _dialog_directory_save(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade:
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        file_dialog = QFileDialog()
        # file_dialog.setFilter("Sment files (*.sment *.zip)")
        directory_output = file_dialog.getExistingDirectory(
            caption='Save Blueprint',
            directory=blueprint_dir,
            options=options)

        if not directory_output:
            return
        msg_input_invalid = "Invalid Blueprint directory path: '{}'".format(directory_output)
        if not Validator().validate_dir(directory_output, only_parent=True):
            # messagebox.showwarning("Blueprint", msg_input_invalid)
            self._window.status_bar.showMessage("Error: {}".format(msg_input_invalid))
            return
        if os.path.exists(directory_output):
            if len(os.listdir(directory_output)) > 0:
                msg_input_invalid = "Output directory is not empty, aborting to prevent overwriting.".format(
                    directory_output)
                # messagebox.showwarning("Blueprint", msg_input_invalid)
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
        # self.text_box.delete(1.0)
        # self.text_box.write(msg)
        # print("Blueprints:", len(self._smbedit.blueprint), self._smbedit.blueprint)
        for index, blueprint in enumerate(self._smbedit.blueprint):
            relative_path = os.path.join(blueprint_name, self._smbedit._directory_input[index])
            blueprint_output = os.path.join(directory_output, self._smbedit._directory_input[index])
            if self._smbedit._directory_input[index] == '':
                relative_path = blueprint_name
                blueprint_output = directory_output
            # self.text_box.delete(2.0)
            # self.text_box.write(, 2.0)
            self._window.status_bar.showMessage("Writing\t'{}'".format(relative_path))
            if not os.path.exists(blueprint_output):
                os.mkdir(blueprint_output)
            blueprint.write(blueprint_output, relative_path)
        # self.text_box.delete("2.0 - 1c")
        # self.text_box.write("Done.\n")
        self._window.status_bar.showMessage(msg + " Done")

    def load_blueprint(self, directory_base):
        self._smbedit.blueprint = []
        self._smbedit._directory_input = []

        blueprint_name = os.path.basename(directory_base)
        msg = "Loading blueprint '{}'... ".format(blueprint_name)
        self._window.status_bar.showMessage(msg)
        # self.text_box.delete(1.0)
        # self.text_box.write("Loading blueprint '{}'... ".format(blueprint_name))
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
            # self.text_box.delete(2.0)
            # self.text_box.write("\n\n", 2.0)
            self._window.status_bar.showMessage("Reading:\t'{}' ...".format(os.path.join(blueprint_name, relative_path)))
            index += 1
            blueprint = Blueprint(entity_name, verbose=False, debug=False)
            blueprint.read(blueprint_path)
            docked_entity_name_prefix = "{}__ATTACHED_".format(entity_name)
            blueprint.replace_outdated_docker_modules(docked_entity_name_prefix, is_docked_entity)
            self._smbedit.blueprint.append(blueprint)
            # relative_path = os.path.relpath(directory_base, os.path.dirname(blueprint_path))
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

        self._main_frame.entities_combo_box.clear()
        self._main_frame.entities_combo_box.addItem('All')
        self._main_frame.entities_check_box.setChecked(False)
        self._window.status_bar.showMessage(msg + " Done")
        # self.text_box.delete("2.0 - 1c")
        # self.text_box.write("Done.\n")
        self._main_frame.update_summary()
        self._main_frame.enable()
