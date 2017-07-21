__author__ = 'Peter Hofmann'
__version__ = '0.1.0'

import os
import sys
import shutil
import tempfile
import argparse
import zipfile

from .validator import Validator
from .configparserwrapper import ConfigParserWrapper


class ArgumentHandler(Validator):
    """
    # #######################################
    # ###  StarMade Blueprint Editor
    # #######################################

    Works with StarMade v0.199.257


    @type _tmp_dir: str
    @type _directory_starmade: str
    """

    def __init__(self, options, label="ArgumentHandler", logfile=None, verbose=False, debug=False):
        """
        Constructor of Argumenthandler

        @param logfile: file handler or file path to a log file
        @type logfile: file | FileIO | StringIO | str
        @param verbose: Not verbose means that only warnings and errors will be past to stream
        @type verbose: bool
        @param debug: Display debug messages
        @type debug: bool

        @rtype: None
        """
        self._tmp_dir = None
        config_file_path = self.get_config_file_path()
        super(ArgumentHandler, self).__init__(
            label=label,
            logfile=logfile,
            verbose=verbose,
            debug=debug)
        self._docked_entities = options.docked_entities
        self._path_input = options.path_input
        self._path_output = options.path_output
        self._link_salvage = options.link_salvage
        self._index_turn_tilt = None  # options.turn
        self._reset_hull_shape = options.reset_hull_shape
        self._replace_hull = options.replace_hull_blocks
        self._replace = options.replace
        self._remove_blocks = None
        remove_blocks = options.remove_blocks
        self._move_center = options.move_center
        mirror_axis = options.mirror_axis
        self._mirror_axis = None
        self._update = options.update
        self._auto_hull_shape = (options.auto_wedge, options.auto_tetra, options.auto_corner, options.auto_hepta)
        self._entity_type = options.entity_type
        self._entity_class = options.entity_class
        self._summary = options.summary
        temp_directory = options.tmp_dir
        if self._path_input is not None:
            self._path_input = self.get_full_path(self._path_input)
        if self._path_output is not None:
            self._path_output = self.get_full_path(self._path_output)

        # deal with StarMade directory
        msg_bad_sm_dir = "Bad StarMade directory: '{}'."
        self._directory_starmade = options.starmade_dir
        if self._directory_starmade is not None:
            self._directory_starmade = self.get_full_path(self._directory_starmade)
            assert self.validate_dir(
                self._directory_starmade, file_names=["StarMade.jar"], key='-sm', silent=True), msg_bad_sm_dir.format(
                self._directory_starmade)
        config = ConfigParserWrapper(logfile=logfile, verbose=verbose)
        if self.validate_file(config_file_path, silent=True):
            config.read(config_file_path)
        option = "starmade_dir"
        section = "main"
        if self._directory_starmade is None:
            self._directory_starmade = config.get_value(option, section, is_path=True, silent=True)
            if self._directory_starmade:
                if not self.validate_dir(self._directory_starmade, file_names=["StarMade.jar"], key='-sm'):
                    config.set_value(option, "", section)
                    config.write(config_file_path)
        if self._directory_starmade is not None:
            if not self.validate_dir(self._directory_starmade, file_names=["StarMade.jar"], key='-sm', silent=True):
                self._logger.warning(msg_bad_sm_dir.format(self._directory_starmade))
                self._directory_starmade = None
            else:
                config.set_value(option, self._directory_starmade, section)
                config.write(config_file_path)

        # deal with temporary directory
        if temp_directory is None:
            self._tmp_dir = tempfile.mkdtemp(prefix="{}_".format(label))
        else:
            assert self.validate_dir(temp_directory)
            self._tmp_dir = tempfile.mkdtemp(prefix="{}_".format(label), dir=temp_directory)

        # deal with input directory
        if self._path_input.endswith(".sment"):
            assert self.validate_file(self._path_input)
            assert zipfile.is_zipfile(self._path_input)
            self._directory_input = tempfile.mkdtemp(dir=self._tmp_dir)
            with zipfile.ZipFile(self._path_input, "r") as read_handler:
                read_handler.extractall(self._directory_input)
            list_of_dir = os.listdir(self._directory_input)
            assert len(list_of_dir) == 1, "Invalid sment file"
            blueprint_name = list_of_dir[0]
            self._directory_input = os.path.join(self._directory_input, blueprint_name)
        else:
            self._directory_input = self._path_input
        file_names = ["header.smbph", "logic.smbpl", "meta.smbpm"]
        msg_input_invalid = "Blueprint input path is invalid, aborting."
        assert self.validate_dir(self._directory_input, file_names=file_names), msg_input_invalid

        # deal with output directory
        self._directory_output_tmp = None
        if self._path_output is not None:
            assert self.validate_dir(self._path_output, only_parent=True)
            msg_output_exists = "Output location exists. Overwriting is not allowed, aborting."
            if self._path_output.endswith(".sment"):
                assert not self.validate_file(self._path_output, silent=True), msg_output_exists
                blueprint_name = os.path.splitext(os.path.basename(self._path_output))[0]
            else:
                blueprint_name = os.path.basename(self._path_output)
                if self.validate_dir(self._path_output, silent=True):
                    if len(os.listdir(self._path_output)) > 0:
                        raise RuntimeError(msg_output_exists)
            self._directory_output_tmp = os.path.join(tempfile.mkdtemp(dir=self._tmp_dir), blueprint_name)

        # deal with something else
        if remove_blocks is not None:
            try:
                self._remove_blocks = list(map(int, remove_blocks.split(',')))
            except ValueError:
                raise ValueError("Bad block id in: '{}'".format(self._remove_blocks))
        if mirror_axis is not None:
            axis = ['x', 'y', 'z']
            if 'r' in mirror_axis:
                assert len(mirror_axis) == 2, "Invalid mirror argument: '{}'".format(mirror_axis)
                reverse = True
                mirror_axis = mirror_axis.strip('r')
            else:
                assert len(mirror_axis) == 1, "Invalid mirror argument: '{}'".format(mirror_axis)
                reverse = False
            assert mirror_axis in axis, "Invalid mirror axis: '{}'".format(mirror_axis)
            self._mirror_axis = (axis.index(mirror_axis), reverse)

    def __exit__(self, type, value, traceback):
        super(ArgumentHandler, self).__exit__(type, value, traceback)
        if self.validate_dir(self._tmp_dir, silent=True):
            shutil.rmtree(self._tmp_dir)
        self.tmp_dir = None

    def __del__(self):
        super(ArgumentHandler, self).__del__()
        if self.validate_dir(self._tmp_dir, silent=True):
            shutil.rmtree(self._tmp_dir)
        self.tmp_dir = None

    # #######################################
    # ###  Read command line arguments
    # #######################################

    _char_to_hull_type = {
        'h': 0,
        's': 1,
        'a': 2,
        'c': 3,
        'z': 4,
    }

    @staticmethod
    def get_parser_options(args=None, label="NoName", version="Prototype"):
        """
        Parsing of passed arguments.

        @param args: Arguments like sys.argv

        @rtype: any
        """
        parser = argparse.ArgumentParser(
            usage="python %(prog)s directory_blueprint",
            description="""
    #######################################
    #    {label}#
    #    Version: {version}#
    #######################################

    A StarMade blueprints editor""".format(
                label=label.ljust(33),
                version=version.ljust(24)
            ),
            formatter_class=argparse.RawTextHelpFormatter)

        group_input = parser.add_argument_group('Required')
        group_input.add_argument(
            "path_input",
            type=str,
            help="Directory of a blueprint or '*.sment' file path.")

        parser.add_argument('-V', '--version',
                            action='version',
                            version="{label} {version}".format(label=label, version=version),)

        parser.add_argument(
            "-silent", "--silent",
            action='store_true',
            default=False,
            help="Suppress messages to stdout.")
        parser.add_argument(
            "-debug", "--debug_mode",
            action='store_true',
            default=False,
            help="Show debug messages and extensive information.")
        parser.add_argument(
            "-log", "--logfile",
            default=None,
            type=str,
            help="Output will also be written to this log file.")
        parser.add_argument(
            "-tmp", "--tmp_dir",
            default=None,
            type=str,
            help="Directory for temporary data in case of 'sment' files.")

        group_input = parser.add_argument_group('Optional arguments')
        group_input.add_argument(
            "-o", "--path_output",
            default=None,
            type=str,
            help="Output directory of modified blueprint or '*.sment' file path")

        group_input.add_argument(
            "-sm", "--starmade_dir",
            default=None,
            type=str,
            help="Directory path to the StarMade folder, attempting to read block config there.")

        group_input.add_argument(
            "-s", "--summary",
            action='store_true',
            default=False,
            help="Display summary of blueprint.")

        group_input.add_argument(
            "-u", "--update",
            action='store_true',
            default=False,
            help="Remove outdated blocks and replace old docking blocks.")

        group_input.add_argument(
            "-d", "--docked_entities",
            action='store_true',
            default=False,
            help="Apply modifications to docked entities, too.")

        group_input.add_argument(
            "-ls", "--link_salvage",
            action='store_true',
            default=False,
            help="Link salvage modules to salvage computers in checker muster.")

    #     group_input.add_argument(
    #         "-t", "--turn",
    #         default=None,
    #         type=int,
    #         choices=[0, 1, 2, 3, 4, 5],
    #         help='''turn the ship/station:
    #     0: "tilt up",
    #     1: "tilt down",
    #     2: "turn right",
    #     3: "turn left",
    #     4: "tilt right",
    #     5: "tilt left"
    # ''')

        group_input.add_argument(
            "-et", "--entity_type",
            default=None,
            type=int,
            choices=[0, 1, 2, 3, 4],
            help='''Change entity type to:
        0: Ship
        1: Shop
        2: Space Station
        3: Asteroid
        4: Planet
    ''')

        group_input.add_argument(
            "-ec", "--entity_class",
            default=None,
            type=int,
            choices=list(range(9)),
            help='''Change entity type to:
            0: General
            1: Mining
            2: Support / Trade
            3: Cargo / Shopping
            4: Attack / Outpost
            5: Defence
            6: Carrier / Shipyard
            7: Scout / Warp Gate
            8: Scavenger / Factory
    ''')

        group_input.add_argument(
            "-m", "--move_center",
            default=None,
            type=str,
            help="Either a block id or a directional vector like '0,0,1', for moving center (Core) one block forward.")

        group_input.add_argument(
            "-ma", "--mirror_axis",
            default=None,
            choices=['x', 'y', 'z', 'xr', 'yr', 'zr'],
            type=str,
            help='''Mirror entity at core/center at a specific axis:
            x Left to Right
            y Top to Bottom
            z Front to Back
     ''')

        group_auto_shape = parser.add_argument_group('Auto shape')
        group_auto_shape.add_argument(
            "-aw", "--auto_wedge",
            action='store_true',
            default=False,
            help="Automatically replace hull blocks with wedges on edge blocks.")

        group_auto_shape.add_argument(
            "-at", "--auto_tetra",
            action='store_true',
            default=False,
            help="Automatically replace hull blocks with tetras at corner blocks.")

        group_auto_shape.add_argument(
            "-ah", "--auto_hepta",
            action='store_true',
            default=False,
            help="Automatically smooth out blocks cornered by wedges, tetra and corners.")

        group_auto_shape.add_argument(
            "-ac", "--auto_corner",
            action='store_true',
            default=False,
            help="Automatically replace hull blocks with corners at corner blocks.")

        group_replace = parser.add_argument_group('Replace blocks')
        group_replace.add_argument(
            "-rs", "--reset_hull_shape",
            action='store_true',
            default=False,
            help="Set outer ship hull blocks to cube.")

        group_replace.add_argument(
            "-rm", "--remove_blocks",
            default=None,
            type=str,
            help="Remove all blocks of the given block id.")

        group_replace.add_argument(
            "-r", "--replace",
            default=None,
            type=str,
            help="""'old_id:new_id'
            Use '-sm' argument to ensure correct hit point for replaced block.""")

        group_replace.add_argument(
            "-rh", "--replace_hull_blocks",
            default=None,
            type=str,
            help='''{h,s,a,c,z}:{h,s,a,c,z}
            h: Hull
            s: Standard armor
            a: Advanced Armor
            c: Crystal Armor
            z: Hazard Armor''')

        if args is None:
            return parser.parse_args()
        else:
            return parser.parse_args(args)

    @staticmethod
    def get_config_file_path():
        app_name = ".SMBEdit"
        file_name_config = "config.ini"
        if sys.platform == "win32":
            app_name = "SMBEdit"
            root_dir = os.getenv("APPDATA")
        else:
            root_dir = ArgumentHandler.get_full_path("~")
            if sys.platform == "darwin":
                app_name = "SMBEdit"
                root_dir = os.path.join(root_dir, "Library", "Application Support")
        assert os.path.exists(root_dir)
        assert os.path.isdir(root_dir)
        app_dir = os.path.join(root_dir, app_name)
        if not os.path.exists(app_dir):
            os.mkdir(app_dir)
        return os.path.join(app_dir, file_name_config)
