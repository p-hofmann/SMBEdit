__author__ = 'Peter Hofmann'


import sys
import os
import zipfile
import tempfile
from ...validator import Validator
from ...blueprint import Blueprint
from smbedit import SMBEdit
if sys.version_info < (3,):
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
else:
    from tkinter import messagebox, filedialog


class ActionMenuBar(Validator):
    """
    @type _smbedit: smbeditGUI.SMBEditGUI
    """

    _file_types = [
        ("Blueprint", "*.sment"),
        ("Blueprint", "*.zip")
        ]

    def __init__(self, root_frame, smbedit, logfile=None, verbose=False, debug=False):
        """

        @type root_frame: smlib.gui.frames.mainframe.MainFrame
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        # RootFrame.__init__(self, root, smbedit)
        self._smbedit = smbedit
        self.root_frame = root_frame
        super(Validator, self).__init__(label="MenuBar", logfile=logfile, verbose=verbose, debug=debug)

        self.root_frame.menubar.menu_cascade_load.add_command(
            label="Load blueprint", command=self._dialog_directory_load)
        self.root_frame.menubar.menu_cascade_load.add_command(
            label="Load *.sment", command=self._dialog_file_load)
        self.root_frame.menubar.menu_cascade_save.add_command(
            label="Save blueprint", command=self._dialog_directory_save)
        self.root_frame.menubar.menu_cascade_save.add_command(
            label="Save *.sment", command=self._dialog_file_save)

    def _dialog_file_load(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade:
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')
        file_path = filedialog.askopenfilename(
            filetypes=ActionMenuBar._file_types, initialdir=blueprint_dir)
        if not file_path:
            return
        if not self.validate_file(file_path):
            return
        if not self.validate_file(file_path, silent=True):
            messagebox.showwarning("Blueprint", "Invalid sment file.")
            return
        if not zipfile.is_zipfile(file_path):
            messagebox.showwarning("Blueprint", "Not a zip compressed file.")
            return

        tmp_directory_input = tempfile.mkdtemp(dir=self._smbedit.tmp_dir)
        with zipfile.ZipFile(file_path, "r") as read_handler:
            read_handler.extractall(tmp_directory_input)
        list_of_dir = os.listdir(tmp_directory_input)
        if len(list_of_dir) != 1:
            messagebox.showwarning("Blueprint", "Invalid sment file content.")
            return
        blueprint_name = list_of_dir[0]
        directory_input = os.path.join(tmp_directory_input, blueprint_name)
        self.load_blueprint(directory_input)

    def _dialog_file_save(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade:
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')
        file_path = filedialog.asksaveasfilename(
            defaultextension=".sment", filetypes=ActionMenuBar._file_types, initialdir=blueprint_dir)
        if not file_path:
            return
        if not self.validate_dir(file_path, only_parent=True):
            messagebox.showwarning("Blueprint", "Invalid directory.")
            return

        blueprint_name = os.path.splitext(os.path.basename(file_path))[0]
        directory_output = os.path.join(tempfile.mkdtemp(dir=self._smbedit.tmp_dir), blueprint_name)
        self.save_blueprint(directory_output)
        SMBEdit.zip_directory(directory_output, file_path)

    def _dialog_directory_load(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade:
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')
        directory_input = filedialog.askdirectory(mustexist=True, initialdir=blueprint_dir)
        if not directory_input:
            return
        file_names = ["header.smbph", "logic.smbpl", "meta.smbpm"]
        msg_input_invalid = "Blueprint input is invalid: '{}'".format(os.path.basename(directory_input))
        if not self.validate_dir(directory_input, file_names=file_names):
            messagebox.showwarning("Blueprint", msg_input_invalid)
            return
        directory_input = directory_input
        self.load_blueprint(directory_input)

    def _dialog_directory_save(self):
        blueprint_dir = None
        if self._smbedit.directory_starmade:
            blueprint_dir = os.path.join(self._smbedit.directory_starmade, 'blueprints')
        directory_output = filedialog.askdirectory(mustexist=False, initialdir=blueprint_dir)
        if not directory_output:
            return
        msg_input_invalid = "Invalid Blueprint directory path: '{}'".format(directory_output)
        if not self.validate_dir(directory_output, only_parent=True):
            messagebox.showwarning("Blueprint", msg_input_invalid)
            return
        if os.path.exists(directory_output):
            if len(os.listdir(directory_output)) > 0:
                msg_input_invalid = "Output directory is not empty, aborting to prevent overwriting.".format(
                    directory_output)
                messagebox.showwarning("Blueprint", msg_input_invalid)
                return
        directory_output = directory_output
        self.save_blueprint(directory_output)

    # #################
    # Load Save
    # #################

    def save_blueprint(self, directory_output):
        directory_output = self.get_full_path(directory_output)
        blueprint_name = os.path.basename(directory_output)
        msg = "Saving blueprint '{}'... ".format(blueprint_name)
        self.root_frame.status_bar.set(msg)
        # self.text_box.delete(1.0)
        # self.text_box.write(msg)
        for index, blueprint in enumerate(self._smbedit.blueprint):
            relative_path = os.path.join(blueprint_name, self._smbedit._directory_input[index])
            blueprint_output = os.path.join(directory_output, self._smbedit._directory_input[index])
            if self._smbedit._directory_input[index] == '':
                relative_path = blueprint_name
                blueprint_output = directory_output
            # self.text_box.delete(2.0)
            # self.text_box.write(, 2.0)
            self.root_frame.status_bar.set("Writing\t'{}'".format(relative_path))
            if not os.path.exists(blueprint_output):
                os.mkdir(blueprint_output)
            blueprint.write(blueprint_output, relative_path)
        # self.text_box.delete("2.0 - 1c")
        # self.text_box.write("Done.\n")
        self.root_frame.status_bar.set(msg + " Done")

    def load_blueprint(self, directory_base):
        self._smbedit.blueprint = []
        self._smbedit._directory_input = []

        blueprint_name = os.path.basename(directory_base)
        msg = "Loading blueprint '{}'... ".format(blueprint_name)
        self.root_frame.status_bar.set(msg)
        # self.text_box.delete(1.0)
        # self.text_box.write("Loading blueprint '{}'... ".format(blueprint_name))
        directory_base = self.get_full_path(directory_base)
        index = 0
        is_docked_entity = False
        tmp_list_path = list()
        self.root_frame.list_of_entity_names = list()
        tmp_list_path.append(directory_base)
        self.root_frame.list_of_entity_names.append("MAIN")
        while index < len(tmp_list_path):
            blueprint_path = tmp_list_path[index]
            entity_name = self.root_frame.list_of_entity_names[index]
            relative_path = os.path.relpath(blueprint_path, directory_base)
            if relative_path == '.':
                relative_path = ''
            self._smbedit._directory_input.append(relative_path)
            if relative_path == '':
                relative_path = blueprint_name
            # self.text_box.delete(2.0)
            # self.text_box.write("\n\n", 2.0)
            self.root_frame.status_bar.set("Reading:\t'{}'".format(os.path.join(blueprint_name, relative_path)))
            index += 1
            blueprint = Blueprint(entity_name, logfile=self._logfile, verbose=self._verbose, debug=self._debug)
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
                self.root_frame.list_of_entity_names.append("{}{}".format(docked_entity_name_prefix, dock_index))

        self.root_frame.entities_combo_box['values'] = ['All']
        self.root_frame.entities_combo_box.current(0)
        self.root_frame.entities_variable_checkbox.set(0)
        self.root_frame.status_bar.set(msg + " Done")
        # self.text_box.delete("2.0 - 1c")
        # self.text_box.write("Done.\n")
        self.root_frame.update_summary(self._smbedit)

    # @StandardError
    # def _dialog_file_save(self):
    #     return filedialog.asksaveasfilename(filetypes=SMBEditGUI._file_types)
