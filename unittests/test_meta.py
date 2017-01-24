from unittest import TestCase
from StringIO import StringIO
from lib.smblueprint.meta.meta import Meta
from lib.bits_and_bytes import BinaryStream
import os

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Meta
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None
        self._blueprints = set()
        self._file_name = "meta.smbpm"

    def get_blueprints(self, directory_blueprints):
        list_of_stuff = os.listdir(directory_blueprints)
        for name in list_of_stuff:
            path = os.path.join(directory_blueprints, name)
            if not os.path.isdir(path):
                continue
            file_path = os.path.join(path, self._file_name)
            if not os.path.exists(file_path):
                continue
            self._blueprints.add(path)

    def setUp(self):
        # block_config.from_hard_coded()
        self.object = Meta()
        directory_blueprints = "/home/hofmann/Downloads/starmade-launcher-linux-x64/StarMade/blueprints"
        self.get_blueprints(directory_blueprints)

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestMeta(DefaultSetup):
    def test__read_file(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)

    def test__write_dummy(self):
        input_stream = BinaryStream(StringIO())
        self.object._write_dummy(input_stream)

    def test__write_file(self):
        input_stream = BinaryStream(StringIO())
        self.object._write_file(input_stream, "./")

    def test_move_center_by_vector(self):
        self.fail()
