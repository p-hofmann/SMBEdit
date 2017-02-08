from unittest import TestCase
from lib.smblueprint.smdblock.block import Block
from lib.utils.blockconfig import block_config

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Block
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None

    def setUp(self):
        block_config.from_hard_coded()
        # wedge 599 0, 0, 0, 3
        # corner 600
        # hepta 601
        # tetra 602
        self.default_orientation = (0, 1, 0, 3)
        self.object = Block().get_modification(
            block_id=599,
            hit_points=75,
            active=None,
            block_side_id=None,
            bit_19=self.default_orientation[0],
            bit_23=self.default_orientation[1],
            bit_22=self.default_orientation[2],
            rotations=self.default_orientation[3]
        )

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestBlock(DefaultSetup):
    def test_get_id(self):
        self.assertEqual(self.object.get_id(), 599)

    def test_get_hit_points(self):
        self.assertEqual(self.object.get_hit_points(), 75)

    def test_get_style(self):
        self.assertEqual(self.object.get_style(), 1)

    def test_is_active(self):
        self.assertFalse(self.object.is_active())

    def test__get_active_value(self):
        self.assertEqual(self.object._get_active_value(), 0)

    def test_get_orientation(self):
        expected_orientation = self.default_orientation
        self.assertTupleEqual(self.object.get_orientation().get_orientation_values(), expected_orientation)

    def test_int_24bit(self):
        int24 = 123456
        self.object = Block(int24)
        self.assertEqual(self.object.get_int_24bit(), int24)

    def test_convert_to_type_6(self):
        expected_orientation = (0, 0, 0, 2)
        self.object = Block(0).get_modification(block_id=7)
        self.object = self.object.get_converted_to_type_6()
        self.assertTupleEqual(self.object.get_orientation().get_orientation_values(), expected_orientation)

    def test_set_id(self):
        self.object = self.object.get_modification(block_id=604)
        self.assertEqual(self.object.get_id(), 604)

    def test_set_hit_points(self):
        self.object = self.object.get_modification(hit_points=50)
        self.assertEqual(self.object.get_hit_points(), 50)

    # def test_set_active(self):
    #     self.assertRaises(AssertionError, self.object.set_active, True)

    def test_mirror(self):
        self.object = self.object.get_mirror(0)
        expected_orientation = (0, 1, 0, 1)
        self.assertTupleEqual(self.object.get_orientation().get_orientation_values(), expected_orientation)
