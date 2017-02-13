from unittest import TestCase
from smbedit import SMBEdit
from unittests.blueprints import blueprint_handler
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

    def setUp(self):
        block_config.from_hard_coded()
        self.object = None

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestSMBEdit(DefaultSetup):
    def test_run(self):
        for blueprint in self._blueprints:
            options = Options(path_input=blueprint)
            with SMBEdit(
              options=options,
              logfile=None,
              verbose=False,
              debug=True) as manipulator:
              manipulator.run()


class Options(object):

    def __init__(self, starmade_dir=None, path_input=None):
        self.starmade_dir = starmade_dir
        self.path_input = path_input
        self.path_output = None
        self.docked_entities = None
        self.link_salvage = None
        self.turn = None
        self.replace_hull = None
        self.replace = None
        self.remove_blocks = None
        self.move_center = None
        self.mirror_axis = None
        self.mirror_axis = None
        self.update = None
        self.auto_wedge = None
        self.auto_tetra = None
        self.auto_corner = None
        self.auto_hepta = None
        self.entity_type = None
        self.entity_class = None
        self.summary = None
        self.tmp_dir = None
