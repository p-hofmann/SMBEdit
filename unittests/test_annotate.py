import os
from unittest import TestCase
# from unittests.blueprints import Blueprint
from lib.utils.blockconfig import block_config
from lib.utils.annotate import Annotate
from lib.utils.periphery import Periphery
# from lib.utils.vector import Vector
from lib.smblueprint.smd3.smd import Smd

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Annotate
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None
        self._blueprint = os.path.join("test_blueprints", "B_Ball")

    def setUp(self):
        block_config.from_hard_coded()
        smd = Smd()
        smd.read(self._blueprint)
        periphery = Periphery(smd.get_block_list())
        self.object = Annotate(smd.get_block_list(), periphery)
        self.min_position, self.max_position = smd.get_min_max_vector()

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestAnnotate(DefaultSetup):
    def test_flood(self):
        # inside
        start_position = (16, 17, 16)
        inside_marked, inside_border = self.object.flood(start_position, self.min_position, self.max_position)
        # self.assertEqual(len(inside_marked), 5 * 5 * 5 - 1)
        # self.assertEqual(len(inside_border), 5 * 5 * 6 + 1)
        self.assertEqual(len(inside_marked), 72)
        self.assertEqual(len(inside_border), 91)

        # outside
        start_position = self.min_position
        outside_marked, outside_border = self.object.flood(start_position, self.min_position, self.max_position)
        self.assertEqual(len(outside_marked), 1026)  # 9 * 9 * 9 - border - box
        self.assertEqual(len(outside_border), 134)

    def test_get_boundaries(self):
        # inside
        min_position = self.min_position
        max_position = self.max_position
        # min_position = Vector.subtraction(self.min_position, (1, 1, 1))
        # max_position = Vector.addition(self.max_position, (1, 1, 1))

        # outside
        start_position = self.min_position
        outside_marked, outside_border = self.object.flood(start_position, min_position, max_position)
        # outside
        # start_position = self.min_position
        marked, border = self.object.get_boundaries(min_position, max_position)
        special_position = self.object._block_list.get_index((18, 17, 18))
        self.assertIn(special_position, border)
        # self.assertIn(special_position, outside_border)
        self.assertEqual(len(marked), len(outside_marked))
        self.assertEqual(len(border), len(outside_border))
