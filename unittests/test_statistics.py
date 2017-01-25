from unittest import TestCase
from io import BytesIO
from lib.bits_and_bytes import BinaryStream
from lib.smblueprint.header import Statistics
# from lib.blueprint.smd3.smd import Smd

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Statistics
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None

    def setUp(self):
        self.object = Statistics()

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestStatistics(DefaultSetup):
    def test_bad_version(self):
        stream = BinaryStream(BytesIO())
        stream.write_bool(True)
        stream.write_int16_unassigned(2)
        stream.seek(0)
        self.assertRaises(AssertionError, self.object.read, stream)

    def test_read_write_empty(self):
        stream = BinaryStream(BytesIO())
        self.object.write(stream)
        stream.seek(0)
        self.object.read(stream)
        self.assertFalse(self.object.has_statistics)

    def test_read_write_data(self):
        stream = BinaryStream(BytesIO())
        self.object.has_statistics = True
        self.object.write(stream)
        self.object.has_statistics = False
        stream.seek(0)
        self.object.read(stream)
        self.assertTrue(self.object.has_statistics)
