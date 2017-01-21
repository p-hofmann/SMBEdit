from unittest import TestCase
from StringIO import StringIO
from lib.bits_and_bytes import ByteStream
from lib.blueprint.header import Header
# from lib.blueprint.smd3.smd import Smd

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Header
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None

    def setUp(self):
        self.object = Header()

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestHeader(DefaultSetup):
    def test__read_block_quantities(self):
        block_id_to_quantity = {
            1: 1,
            2: 100
        }
        stream = ByteStream(StringIO())
        stream.write_int32_unassigned(len(block_id_to_quantity))
        for block_id in block_id_to_quantity:
            stream.write_int16_unassigned(block_id)
            stream.write_int32_unassigned(block_id_to_quantity[block_id])
        stream.seek(0)
        self.object._read_block_quantities(stream)
        self.assertDictEqual(self.object.block_id_to_quantity, block_id_to_quantity)

    def test__read_header(self):
        self.fail()

    def test__read_file(self):
        self.fail()

    def test_read(self):
        self.fail()

    def test__write_block_quantities(self):
        self.fail()

    def test__write_header(self):
        self.fail()

    def test__write_file(self):
        self.fail()

    def test_write(self):
        self.fail()

    def test_iteritems(self):
        self.fail()

    def test__get_measure(self):
        self.fail()

    def test_get_type_name(self):
        self.fail()

    def test_get_classification_name(self):
        self.fail()

    def test_get_width(self):
        self.fail()

    def test_get_height(self):
        self.fail()

    def test_get_length(self):
        self.fail()

    def test_add(self):
        self.fail()

    def test_set_class(self):
        self.fail()

    def test_set_type(self):
        self.fail()

    def test_set_quantities(self):
        self.fail()

    def test_update(self):
        self.fail()

    def test_remove(self):
        self.fail()

    def test_set_box(self):
        self.fail()

    def test_to_stream(self):
        self.fail()
