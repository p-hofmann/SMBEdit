import os
from unittest import TestCase
# from unittests.blueprints import Blueprint
from smlib.utils.blockconfig import block_config
from smlib.utils.annotate import Annotate
from smlib.utils.periphery import Periphery
from smlib.utils.vector import Vector
from smlib.smblueprint.smd3.smd import Smd
from unittests.blueprints import blueprint_handler


__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self._blueprint = blueprint_handler

    def setUp(self):
        block_config.from_hard_coded()

    def tearDown(self):
        return


class TestAnnotate(DefaultSetup):
    def test_flood(self):
        blueprint = blueprint_handler.extract_sment(os.path.join(".", "test_blueprints", "B_Ball.sment"))
        smd = Smd()
        smd.read(blueprint)
        periphery = Periphery(smd.get_block_list())
        annotate_flood = Annotate(smd.get_block_list(), periphery)
        min_position, max_position = smd.get_min_max_vector()
        # inside
        start_position = (16, 17, 16)
        annotate_flood.flood(start_position, min_position, max_position)
        inside_marked, inside_border = annotate_flood.get_data()
        # self.assertEqual(len(inside_marked), 5 * 5 * 5 - 1)
        # self.assertEqual(len(inside_border), 5 * 5 * 6 + 1)
        self.assertEqual(len(inside_marked), 72)
        self.assertEqual(len(inside_border), 163)

        # outside
        start_position = Vector.subtraction(min_position, (1, 1, 1))
        annotate_flood.flood(start_position, min_position, max_position)
        outside_marked, outside_border = annotate_flood.get_data()
        self.assertEqual(len(outside_marked), 1026)  # 9 * 9 * 9 - border - box
        self.assertEqual(len(outside_border), 218)

    def test_get_boundaries(self):
        smd = Smd()
        for blueprint_dir in blueprint_handler:
            # flood
            smd.read(blueprint_dir)
            # hull_blocks = 0
            # for block_id, amount in smd.get_block_id_to_quantity().items():
            #     if block_config[block_id].tier is not None:
            #         hull_blocks += amount
            # print(blueprint_dir, hull_blocks)
            periphery = Periphery(smd.get_block_list())
            annotate = Annotate(smd.get_block_list(), periphery)
            min_position, max_position = smd.get_min_max_vector()
            start_position = Vector.subtraction(min_position, (1, 1, 1))
            annotate.flood(start_position, min_position, max_position)
            annotate.remove_empty_voxel()
            outside_marked, outside_border = annotate.get_data()

            # calc_boundaries
            annotate.calc_boundaries(min_position, max_position)
            annotate.remove_empty_voxel()
            marked, border = annotate.get_data()
            # self.assertIn(special_position, outside_border)
            # print(len(marked), len(border))
            self.assertEqual(len(border), len(outside_border), blueprint_dir)
            self.assertEqual(len(marked), len(outside_marked), blueprint_dir)

    # def test_get_neighbours(self):
    #     start_position = (0, 0, 0)
    #     for position in self.object.get_neighbours(start_position):
    #         print(position)
