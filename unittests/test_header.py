from unittest import TestCase
from StringIO import StringIO
from lib.bits_and_bytes import BinaryStream
from lib.smblueprint.header import Header
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
        self.object.add(88, 100)
        self.object.classification = 1
        self.object.box_min = [-2, -2, -2]
        self.object.box_max = [2, 2, 2]
        self.object.type = 0

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestHeader(DefaultSetup):
    def test__read_block_quantities(self):
        self.object.remove(88)
        block_id_to_quantity = {
            1: 1,
            2: 100
        }
        stream = BinaryStream(StringIO())
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
        self.assertEqual(self.object._get_measure(0), 4)

    def test_get_type_name(self):
        self.assertEqual(self.object.get_type_name(), "Ship")

    def test_get_classification_name(self):
        self.assertEqual(self.object.get_classification_name(), "General")

    def test_get_width(self):
        self.assertEqual(self.object.get_width(), 4)

    def test_get_height(self):
        self.assertEqual(self.object.get_height(), 4)

    def test_get_length(self):
        self.assertEqual(self.object.get_length(), 4)

    def test_add(self):
        self.object.add(88, 100)
        self.object.add(80, 100)
        self.assertEqual(len(self.object.block_id_to_quantity), 2)
        self.assertEqual(self.object.block_id_to_quantity[88], 200)
        self.assertEqual(self.object.block_id_to_quantity[80], 100)

    def test_set_class(self):
        self.object.set_class(5)
        self.assertRaises(AssertionError, self.object.set_class, 15)

    def test_set_type(self):
        self.object.set_type(2)
        self.assertEqual(self.object.classification, 0)
        self.assertRaises(AssertionError, self.object.set_type, 15)

    def test_set_quantities(self):
        self.object.remove(88)
        block_id_to_quantity = {
            1: 1,
            2: 100
        }
        self.object.set_quantities(block_id_to_quantity)
        self.assertDictEqual(self.object.block_id_to_quantity, block_id_to_quantity)

    def test_update(self):
        self.object.update()
        self.assertEqual(len(self.object.block_id_to_quantity), 0)

    def test_remove(self):
        self.object.remove(88)
        self.assertEqual(len(self.object.block_id_to_quantity), 0)
