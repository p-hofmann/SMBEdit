import tempfile
import sys

from PyQt5.QtWidgets import QApplication
from smlib import __version__ as version
from smlib.common.validator import Validator
from smlib.common.configparserwrapper import ConfigParserWrapper
from smlib.common.argumenthandler import ArgumentHandler
from smlib.utils.blockconfig import block_config
from smlib.blueprint import Blueprint
from smlib.gui.window import Window
# from smlib.gui.window import Window


class SMBEditGUI(Validator):
    """
    @type tmp_dir: str
    @type _directory_input: list[str]
    @type blueprint: list[Blueprint]
    """

    def __init__(self, temp_directory=None, logfile=None, verbose=False, debug=False):
        self.tmp_dir = None
        label = "SMBEditGUI " + version
        super(Validator, self).__init__(label=label, logfile=logfile, verbose=verbose, debug=debug)

        # deal with temporary directory
        if temp_directory is None:
            self.tmp_dir = tempfile.mkdtemp(prefix="{}_".format(label))
        else:
            assert self.validate_dir(temp_directory)
            self.tmp_dir = tempfile.mkdtemp(prefix="{}_".format(label), dir=temp_directory)

        self.directory_starmade = self._get_starmade_directory()
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

    def _get_starmade_directory(self):
        # deal with StarMade directory
        config_file_path = ArgumentHandler.get_config_file_path()

        # msg_bad_sm_dir = "Bad StarMade directory: '{}'."
        config = ConfigParserWrapper(logfile=self._logfile, verbose=self._verbose)
        if self.validate_file(config_file_path, silent=True):
            config.read(config_file_path)
        option = "starmade_dir"
        section = "main"
        directory_starmade = config.get_value(option, section, is_path=True, silent=True)
        if directory_starmade and not self.validate_dir(directory_starmade, file_names=["StarMade.jar"], key='-sm'):
            config.set_value(option, "", section)
            config.write(config_file_path)
            return None
        return directory_starmade

    def save_starmade_directory(self, directory_starmade):
        config_file_path = ArgumentHandler.get_config_file_path()
        config = ConfigParserWrapper(logfile=self._logfile, verbose=self._verbose)
        if self.validate_file(config_file_path, silent=True):
            config.read(config_file_path)
        option = "starmade_dir"
        section = "main"
        if directory_starmade and self.validate_dir(directory_starmade, file_names=["StarMade.jar"]):
            config.set_value(option, directory_starmade, section)
            config.write(config_file_path)


def main():
    app = QApplication(sys.argv)
    # QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
    name = "SMBEdit " + version
    with SMBEditGUI(verbose=False, debug=False) as smbedit_gui:
        window = Window(smbedit_gui)
        window.setWindowTitle(name)
        window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
