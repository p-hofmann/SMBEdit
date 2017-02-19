from unittest import TestCase
from smbedit import SMBEdit
from unittests.testinput import blueprint_handler
from lib.utils.blockconfig import block_config

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: SMBEdit
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None
        self._blueprints = blueprint_handler
        self._blueprint_test = ""

    def setUp(self):
        block_config.from_hard_coded()
        self.object = None

    def tearDown(self):
        self.object = None


class TestSMBEdit(DefaultSetup):
    def test_run(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_update(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.update = True
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_summary(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.summary = True
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_move_center(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.move_center = "2,-3,5"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_entity_type(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.entity_type = 2
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_entity_class(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.entity_class = 2
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_replace(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.replace = "598:507"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_remove_blocks(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.remove_blocks = "598,599"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_replace_hull_blocks(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.replace_hull_blocks = ":a"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_reset_hull_shape(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.reset_hull_shape = True
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_mirror_axis_x(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.mirror_axis = "x"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_mirror_axis_xr(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.mirror_axis = "xr"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_mirror_axis_y(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.mirror_axis = "y"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_mirror_axis_yr(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.mirror_axis = "yr"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_mirror_axis_z(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.mirror_axis = "z"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_mirror_axis_zr(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.mirror_axis = "zr"
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_auto_wedge(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.auto_wedge = True
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_auto_tetra(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.auto_tetra = True
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_auto_corner(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.auto_corner = True
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_auto_hepta(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.auto_hepta = True
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)

    def test_auto_shape(self):
        for blueprint in self._blueprints:
            options = Options()
            options.path_input = blueprint
            options.auto_wedge = True
            options.auto_corner = True
            options.auto_tetra = True
            options.auto_hepta = True
            with SMBEdit(
                    options=options,
                    logfile=options.logfile,
                    verbose=options.verbose,
                    debug=options.debug) as manipulator:
                self.assertFalse(manipulator.run(), blueprint)


class Options(object):

    def __init__(self):
        self.logfile = None
        self.verbose = False
        self.debug = True
        self.tmp_dir = None
        self.starmade_dir = None
        self.path_input = None
        self.path_output = None
        self.docked_entities = True
        self.summary = None
        self.silent = True
        self.update = False
        self.turn = None
        self.link_salvage = None

        self.move_center = None

        self.entity_type = None
        self.entity_class = None

        self.remove_blocks = None
        self.reset_hull_shape = False
        self.replace_hull_blocks = None
        self.replace = None

        self.mirror_axis = None

        self.auto_wedge = False
        self.auto_tetra = False
        self.auto_corner = False
        self.auto_hepta = False
