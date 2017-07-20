__author__ = 'Peter Hofmann'

import os
import tempfile

import smbedit
import smlib
from smlib import __version__
from smlib.validator import Validator
from smlib.configparserwrapper import ConfigParserWrapper
from smlib.utils.blockconfig import block_config
from smlib.blueprint import Blueprint
from smlib.gui.window import Window


class SMBEditGUI(Validator):
    """
    @type tmp_dir: str
    @type _directory_input: list[str]
    @type blueprint: list[Blueprint]
    """

    def __init__(self, temp_directory=None, logfile=None, verbose=False, debug=False):
        self.tmp_dir = None
        label = "SMBEdit " + __version__
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
        smbe_dir = os.path.dirname(self.get_full_path(os.path.dirname(smlib.__file__)))
        config_file_path = os.path.join(smbe_dir, "config.ini")

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


def main():
    name = "SMBEdit " + smbedit.__version__
    with SMBEditGUI(verbose=True, debug=True) as smbedit_gui:
        window = Window(smbedit_gui)
        window.resizable(0, 0)
        window.title(name)
        window.mainloop()

if __name__ == "__main__":
    main()
