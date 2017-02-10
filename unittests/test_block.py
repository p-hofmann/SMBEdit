from unittest import TestCase
from lib.smblueprint.smdblock.blockhandler import block_handler, StyleBasic
from lib.utils.blockconfig import block_config

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: StyleBasic
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
        self.default_orientation = (2, 3)
        self.object = block_handler(StyleBasic(599, 3).get_modified_int_24bit(
            block_id=599,
            hit_points=75,
            active=None,
            block_side_id=None,
            # block_side_id=block_side_id,
            axis_rotation=self.default_orientation[0],
            rotations=self.default_orientation[1]
        ))

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestBlock(DefaultSetup):
    """
    @type object: StyleBasic
    """
    def test_get_id(self):
        self.assertEqual(self.object.get_id(), 599)

    def test_get_hit_points(self):
        self.assertEqual(self.object.get_hit_points(), 75)

    def test_get_style(self):
        self.assertEqual(block_config[self.object.get_id()].block_style, 1)

    def test_is_active(self):
        self.assertFalse(self.object.is_active())

    def test__get_active_value(self):
        self.assertEqual(self.object._get_active_bit(), 0)

    def test_get_orientation(self):
        expected_orientation = self.default_orientation
        rotations = self.object.get_rotations()
        axis_rotation = self.object.get_axis_rotation()
        self.assertTupleEqual((axis_rotation, rotations), expected_orientation)

    def test_int_24bit(self):
        int24 = 123456
        self.object = block_handler(int24)
        self.assertEqual(self.object.get_int_24(), int24)

    def test_convert_to_type_6(self):
        expected_orientation = (0, 2)
        self.object = block_handler(block_handler(7).get_modified_int_24bit(block_id=7))
        self.object = block_handler(self.object.to_style6(665))
        rotations = self.object.get_rotations()
        axis_rotation = self.object.get_axis_rotation()
        self.assertTupleEqual((axis_rotation, rotations), expected_orientation)

    def test_set_id(self):
        self.object = block_handler(self.object.get_modified_int_24bit(block_id=604))
        self.assertEqual(self.object.get_id(), 604)

    def test_set_hit_points(self):
        self.object = block_handler(self.object.get_modified_int_24bit(hit_points=50))
        self.assertEqual(self.object.get_hit_points(), 50)

    # def test_set_active(self):
    #     self.assertRaises(AssertionError, self.object.set_active, True)

    def test_mirror(self):
        self.object = block_handler(self.object.get_mirror(0))
        expected_orientation = (2, 1)
        rotations = self.object.get_rotations()
        axis_rotation = self.object.get_axis_rotation()
        self.assertTupleEqual((axis_rotation, rotations), expected_orientation)
