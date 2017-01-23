__author__ = 'Peter Hofmann'
__version__ = '0.1.0'

import os
import shutil
import tempfile
import argparse
import zipfile
from lib.validator import Validator


class ArgumentHandler(Validator):
    """
    # #######################################
    # ###  StarMade Blueprint Editor
    # #######################################

    Works with StarMade v0.199.257


    @type _tmp_dir: str
    """

    def __init__(self, options, logfile=None, verbose=False, debug=False):
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
        super(ArgumentHandler, self).__init__(
            logfile=logfile,
            verbose=verbose,
            debug=debug)
        self._docked_entities = options.docked_entities
        self._path_input = options.path_input
        self._path_output = options.path_output
        self._link_salvage = options.link_salvage
        self._index_turn_tilt = None  # options.turn
        self._replace_hull = options.replace_hull
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
        self._directory_starmade = options.starmade
        self._is_archived = False
        if self._path_input.endswith(".sment"):
            self._is_archived = True

        assert temp_directory is None or self.validate_dir(temp_directory)
        assert self._path_output is None or self.validate_dir(self._path_output, only_parent=True)
        assert self._directory_starmade is None or self.validate_dir(
            self._directory_starmade, file_names=["StarMade.jar"], key='-sm'), "Bad StarMade directory."

        self._directory_output = None
        if self._is_archived:  # .sment file
            assert self.validate_file(self._path_input)
            # .sment file

            if temp_directory is None:
                self._tmp_dir = tempfile.mkdtemp(prefix="{}_".format(self._label))
            else:
                self._tmp_dir = tempfile.mkdtemp(prefix="{}_".format(self._label), dir=temp_directory)

            self._directory_input = tempfile.mkdtemp(dir=self._tmp_dir)
            with zipfile.ZipFile(self._path_input, "r") as read_handler:
                read_handler.extractall(self._directory_input)
            list_of_dir = os.listdir(self._directory_input)
            assert len(list_of_dir) == 1, "Invalid sment file"
            blueprint_name = list_of_dir[0]
            self._directory_input = os.path.join(self._directory_input, blueprint_name)

            if self._path_output is not None:
                assert self._path_output.endswith(".sment"), "Expected '*.sment' file ending."
                assert not self.validate_file(self._path_output, silent=True), "Output file exists. Overwriting files is not allowed, aborting."
                self._directory_output = os.path.join(tempfile.mkdtemp(dir=self._tmp_dir), blueprint_name)
        else:
            self._tmp_dir = None
            self._directory_input = self._clean_dir_path(self._path_input)
            file_names = ["header.smbph", "logic.smbpl", "meta.smbpm"]
            assert self.validate_dir(self._directory_input, file_names=file_names), "Blueprint input path is invalid, aborting."
            if self._path_output is not None:
                self._directory_output = self._clean_dir_path(self._path_output)

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

        group_input = parser.add_argument_group('optional arguments')
        group_input.add_argument(
            "-sm", "--starmade",
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
            "-aw", "--auto_wedge",
            action='store_true',
            default=False,
            help="Automatically replace hull blocks with wedges on edge blocks.")

        group_input.add_argument(
            "-at", "--auto_tetra",
            action='store_true',
            default=False,
            help="Automatically replace hull blocks with tetras at corner blocks.")

        group_input.add_argument(
            "-ah", "--auto_hepta",
            action='store_true',
            default=False,
            help="Automatically smooth out blocks cornered by wedges, tetra and corners.")

        group_input.add_argument(
            "-ac", "--auto_corner",
            action='store_true',
            default=False,
            help="Automatically replace hull blocks with corners at corner blocks.")

        group_input.add_argument(
            "-ls", "--link_salvage",
            action='store_true',
            default=False,
            help="Link salvage computers to salvage modules.")

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
            help='''change entity type to:
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
            help='''change entity type to:
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

        group_input.add_argument(
            "-r", "--replace",
            default=None,
            type=str,
            help="old_id,new_id:hit_points")

        group_input.add_argument(
            "-rm", "--remove_blocks",
            default=None,
            type=str,
            help="Remove all blocks of the given block id.")

        group_input.add_argument(
            "-rh", "--replace_hull",
            default=None,
            type=str,
            help='''{h,s,a,c,z}:{h,s,a,c,z}
            h: Hull
            s: Standard armor
            a: Advanced Armor
            c: Crystal Armor
            z: Hazard Armor''')

        group_input.add_argument(
            "-o", "--path_output",
            default=None,
            type=str,
            help="Output directory of modified blueprint or '*.sment' file path")

        group_input = parser.add_argument_group('required')
        group_input.add_argument(
            "path_input",
            type=str,
            help="Directory of a blue print or sment file path.")

        if args is None:
            return parser.parse_args()
        else:
            return parser.parse_args(args)

    @staticmethod
    def _clean_dir_path(directory):
        return directory.rstrip('/').rstrip('\\')
