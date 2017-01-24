from unittest import TestCase
from StringIO import StringIO
from lib.smblueprint.meta.meta import Meta
from lib.bits_and_bytes import BinaryStream
from blueprints import Blueprint


__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Meta
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None
        self._blueprints = Blueprint()

    def setUp(self):
        # block_config.from_hard_coded()
        self.object = Meta()

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestMeta(DefaultSetup):
    def test_read_file(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)

    def test__write_dummy(self):
        input_stream = BinaryStream(StringIO())
        self.object._write_dummy(input_stream)

    def test__write_file(self):
        input_stream = BinaryStream(StringIO())
        self.object._write_file(input_stream, "./")

    def test_move_center_by_vector(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            self.object.move_center_by_vector((2, 5, 6))
