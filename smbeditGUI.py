import tempfile
import sys

from smlib import __version__ as version
from smlib.common.validator import Validator
from smlib.common.configuration import Configuration
from smlib.utils.blockconfig import block_config
from smlib.blueprint import Blueprint
from smlib.gui.window import Window


class SMBEditGUI(Validator):
    """
    @type tmp_dir: str
    @type _directory_input: list[str]
    @type blueprint: list[Blueprint]
    """

    def __init__(self, configuration, temp_directory=None):
        """

        @param configuration:
        @type configuration: Configuration
        @param temp_directory: directory path
        @type temp_directory: str
        """
        self.tmp_dir = None
        self.configuration = configuration
        label = "SMBEditGUI " + version
        logfile = configuration.get_file_path_log()
        verbose = configuration.verbose
        debug = configuration.debug
        super(SMBEditGUI, self).__init__(
            label=label, logfile=logfile, verbose=verbose, debug=debug)

        # deal with temporary directory
        if temp_directory is None:
            self.tmp_dir = tempfile.mkdtemp(prefix="{}_".format(label))
        else:
            assert self.validate_dir(temp_directory)
            self.tmp_dir = tempfile.mkdtemp(prefix="{}_".format(label), dir=temp_directory)

        self.directory_starmade = self._get_directory_starmade()
        if self.directory_starmade is not None:
            self._logger.debug("StarMade: {}".format(self.directory_starmade))
            block_config.read(self.directory_starmade)
        else:
            block_config.from_hard_coded()

        self.path_input = None
        self.path_output = None
        self._directory_input = []
        self.blueprint = []
        self.blueprint.append(Blueprint("ENTITY_Main", logfile=logfile, verbose=verbose, debug=debug))
        self._directory_input.append('')

    def __exit__(self, type, value, traceback):
        super(SMBEditGUI, self).__exit__(type, value, traceback)
        if self.validate_dir(self.tmp_dir, silent=True):
            import shutil
            shutil.rmtree(self.tmp_dir)
        self.tmp_dir = None

    def __del__(self):
        super(SMBEditGUI, self).__del__()
        if self.validate_dir(self.tmp_dir, silent=True):
            import shutil
            shutil.rmtree(self.tmp_dir)
        self.tmp_dir = None

    def _get_directory_starmade(self):
        """
        Deal with StarMade directory

        @rtype: str
        """
        option = "starmade_dir"
        section = "main"
        directory_starmade = self.configuration.get_path(option=option, section=section)
        if directory_starmade and not self.validate_dir(directory_starmade, file_names=["StarMade.jar"], key='-sm'):
            self.configuration.set(option=option, value="", section=section)
            return None
        return directory_starmade

    def _get_directory_import(self):
        """
        Deal with StarMade directory

        @rtype: str
        """
        option = "import_dir"
        section = "main"
        directory_import = self.configuration.get_path(option=option, section=section)
        if directory_import and not self.validate_dir(directory_import):
            self.configuration.set(option=option, value="", section=section)
            return None
        return directory_import

    def save_directory_starmade(self, directory):
        option = "starmade_dir"
        section = "main"
        if directory and self.validate_dir(directory, file_names=["StarMade.jar"]):
            self.configuration.set_path(option=option, value=directory, section=section)

    def save_directory_import(self, directory):
        option = "import_dir"
        section = "main"
        if directory and self.validate_dir(directory):
            self.configuration.set_path(option=option, value=directory, section=section)


def main():
    name = "SMBEdit"
    configuration = Configuration(
        name,
        file_name_config="config.ini",
        file_name_log="log.txt",
        verbose=False,
        debug=False)
    configuration.load()

    try:
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        smbedit_gui = SMBEditGUI(configuration)
        window = Window(smbedit_gui)
        title = name + " " + version
        window.setWindowTitle(title)
        window.show()
        del smbedit_gui
        sys.exit(app.exec_())
    except Exception as e:
        import datetime
        import time
        time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        with open(configuration.get_file_path_log(), 'a') as output_stream:
            output_stream.write("{}: {}\n".format(time_stamp, e))
        sys.exit(1)


if __name__ == "__main__":
    main()
