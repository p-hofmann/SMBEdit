import sys
import os
from .configparserwrapper import ConfigParserWrapper


class Configuration(object):
    """

    @type _name: str
    @type _file_name_config: str
    @type _config_directory: str
    @type verbose: bool
    @type debug: bool
    """
    def __init__(self, name, file_name_config="config.ini", file_name_log="log.txt", verbose=False, debug=False):
        """

        @param name: Will be used as folder name for the configurations in the home directory
        @type name: str
        @param file_name_config: Name of config file
        @type file_name_config: str
        @param file_name_log: File path
        @type file_name_log: str
        @param verbose:
        @type verbose: bool
        @param debug:
        @type debug: bool
        """
        assert isinstance(name, str)
        self._name = name
        self._file_name_config = file_name_config
        self._file_name_log = file_name_log
        self.verbose = verbose
        self.debug = debug
        self._config_directory = self._get_config_directory()
        self._config_handler = ConfigParserWrapper(logfile=self.get_file_path_log(), verbose=verbose)

    def load(self):
        """
        Read config file if it exists

        @rtype: None
        """
        config_file_path = self.get_file_path_config()
        if os.path.exists(config_file_path) and os.path.isfile(config_file_path):
            self._config_handler.read(config_file_path)

    def set(self, option, value, section=None):
        """

        @param option:
        @type option: str
        @param value:
        @type value: any
        @param section:
        @type section: str

        @rtype: None
        """
        config_file_path = self.get_file_path_config()
        self._config_handler.set_value(option=option, value=value, section=section)
        self._config_handler.write(config_file_path)

    def set_path(self, option, value, section=None):
        """

        @param option:
        @type option: str
        @param value:
        @type value: any
        @param section:
        @type section: str

        @rtype: None
        """
        value = ConfigParserWrapper._get_full_path(value)
        config_file_path = self.get_file_path_config()
        self._config_handler.set_value(option=option, value=value, section=section)
        self._config_handler.write(config_file_path)

    def get(self, option, section=None):
        """

        @param option:
        @type option: str
        @param section:
        @type section: str

        @rtype: any
        """
        return self._config_handler.get_value(option=option, section=section, silent=True)

    def get_path(self, option, section=None):
        """

        @param option:
        @type option: str
        @param section:
        @type section: str

        @rtype: any
        """
        return self._config_handler.get_value(option=option, section=section, is_path=True, silent=True)

    def _get_config_directory(self):
        """
        Establish path in home directory, folder is created if it does not exist

        @return: config directory
        @rtype: str
        """
        app_name = "." + self._name
        if sys.platform.startswith("win"):
            app_name = self._name
            root_dir = os.getenv("APPDATA")
        else:
            root_dir = ConfigParserWrapper._get_full_path("~")
            if sys.platform == "darwin":
                app_name = self._name
                root_dir = os.path.join(root_dir, "Library", "Application Support")
        assert os.path.exists(root_dir)
        assert os.path.isdir(root_dir)
        app_dir = os.path.join(root_dir, app_name)
        if not os.path.exists(app_dir):
            os.mkdir(app_dir)
        return app_dir

    def get_file_path_config(self):
        """
        Return config file path

        @return: file path
        @rtype: str
        """
        return os.path.join(self._config_directory, self._file_name_config)

    def get_file_path_log(self):
        """
        Return log file path

        @return: file path
        @rtype: str
        """
        return os.path.join(self._config_directory, self._file_name_log)
