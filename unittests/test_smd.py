from unittest import TestCase
from StringIO import StringIO
from lib.bits_and_bytes import BinaryStream
from lib.smblueprint.smd3.smd import Smd
from blueprints import Blueprint

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Smd
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None
        self._blueprints = Blueprint()

    def setUp(self):
        self.object = Smd()

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestSmd(DefaultSetup):
    def test_read(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)

    def test_get_block_at_position(self):
        self.fail()

    def test_get_region_position_of_position(self):
        self.fail()

    def test_move_center(self):
        self.fail()

    def test_mirror(self):
        self.fail()

    def test_get_number_of_blocks(self):
        self.fail()

    def test_replace_hull(self):
        self.fail()

    def test_replace_blocks(self):
        self.fail()

    def test_update(self):
        self.fail()

    def test_remove_blocks(self):
        self.fail()

    def test_remove_block(self):
        self.fail()

    def test_add(self):
        self.fail()

    def test_has_block_at_position(self):
        self.fail()

    def test_set_type(self):
        self.fail()

    def test_auto_hull_shape(self):
        self.fail()
