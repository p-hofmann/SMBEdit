import os
from unittest import TestCase
# from unittests.blueprints import Blueprint
from lib.utils.blockconfig import block_config
from lib.utils.annotate import Annotate
from lib.smblueprint.smd3.smd import Smd

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Annotate
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None
        self._blueprint = os.path.join("test_blueprints", "B_Box")

    def setUp(self):
        block_config.from_hard_coded()
        smd = Smd()
        smd.read(self._blueprint)
        self.object = Annotate(smd.get_block_list())
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
        self.assertEqual(len(inside_marked), 5 * 5 * 5 - 1)
        self.assertEqual(len(inside_border), 5 * 5 * 6 + 1)

        # outside
        start_position = self.min_position
        marked, border = self.object.flood(start_position, self.min_position, self.max_position)
        self.assertEqual(len(marked), 9 * 9 * 9 - len(inside_marked) - len(inside_border))  # 9 * 9 * 9 - border - box
        self.assertEqual(len(border), len(inside_border)-1)
