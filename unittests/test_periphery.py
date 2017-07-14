# import sys
import os
from unittest import TestCase
from smlib.utils.blockconfig import block_config
from smlib.utils.periphery import Periphery
from smlib.utils.annotate import Annotate
from smlib.smblueprint.smd3.smd import Smd
from unittests.testinput import blueprint_handler


__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Periphery
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None
        self._blueprint = {
            1: blueprint_handler.extract_sment(os.path.join(".", "test_blueprints", "B_Wedge.sment")),
            2: blueprint_handler.extract_sment(os.path.join(".", "test_blueprints", "B_Corner.sment")),
            3: blueprint_handler.extract_sment(os.path.join(".", "test_blueprints", "B_Tetra.sment")),
            # 4: blueprint_handler.extract_sment(os.path.join(".", "test_blueprints", "B_Diamond_Shape.sment")),
            4: blueprint_handler.extract_sment(os.path.join("test_blueprints", "B_Hepta.sment")),
        }

    def setUp(self):
        block_config.from_hard_coded()
        self.object = None

    def tearDown(self):
        tmp = self.object
        self.object = None
        del tmp

        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestPeriphery(DefaultSetup):
    def test_get_periphery_simple_wedge(self):
        shape_id = block_config.get_shape_id("wedge")
        smd = Smd()
        smd.read(self._blueprint[shape_id])
        self.object = Periphery(smd.get_block_list())
        annotation = Annotate(smd.get_block_list(), self.object)
        min_position, max_position = smd.get_min_max_vector()
        annotation.flood(min_position, min_position, max_position)
        marked, border = annotation.get_data()
        # block_list, marked, border
        self.object.set_annotation(marked=marked, border=border)
        periphery = self.object.get_periphery_simple(shape_id)
        self.assertDictEqual(periphery, self.object.peripheries[shape_id])

    def test_get_periphery_simple_tetra(self):
        shape_id = block_config.get_shape_id("tetra")
        smd = Smd()
        smd.read(self._blueprint[shape_id])
        self.object = Periphery(smd.get_block_list())
        annotation = Annotate(smd.get_block_list(), self.object)
        min_position, max_position = smd.get_min_max_vector()
        annotation.flood(min_position, min_position, max_position)
        marked, border = annotation.get_data()
        # block_list, marked, border
        self.object.set_annotation(marked=marked, border=border)
        periphery = self.object.get_periphery_simple(shape_id)
        self.assertDictEqual(periphery, self.object.peripheries[shape_id])

    def test_get_periphery_complex_corner(self):
        shape_id_corner = block_config.get_shape_id("corner")
        smd = Smd()
        smd.read(self._blueprint[shape_id_corner])
        self.object = Periphery(smd.get_block_list())
        annotation = Annotate(smd.get_block_list(), self.object)
        min_position, max_position = smd.get_min_max_vector()
        annotation.calc_boundaries(min_position, max_position)
        marked, border = annotation.get_data()
        # block_list, marked, border
        self.object.set_annotation(marked=marked, border=border)
        periphery_indxes = {}
        for periphery_index, periphery_shape, periphery_orientation, orientation in self.object.get_periphery_complex(shape_id_corner):
            if periphery_index not in periphery_indxes:
                periphery_indxes[periphery_index] = {}
        #     if orientation not in periphery_indxes[periphery_index]:
        #         periphery_indxes[periphery_index][orientation] = [set(), set(), set(), set(), set(), set()]
        #     for index, shape_id in enumerate(periphery_shape):
        #         periphery_indxes[periphery_index][orientation][index].add((shape_id, periphery_orientation[index]))
        #         # periphery_indxes[periphery_index][orientation][index][shape_id].add(periphery_orientation)
        # periphery = {}
        # for periphery_index, orientations in sorted(periphery_indxes.items()):
        #     for orientation, periphery_vectors in orientations.items():
        #         for shape_id_periphery_orientation_0 in periphery_vectors[0]:
        #             for shape_id_periphery_orientation_1 in periphery_vectors[1]:
        #                 for shape_id_periphery_orientation_2 in periphery_vectors[2]:
        #                     for shape_id_periphery_orientation_3 in periphery_vectors[3]:
        #                         for shape_id_periphery_orientation_4 in periphery_vectors[4]:
        #                             for shape_id_periphery_orientation_5 in periphery_vectors[5]:
        #                                 periphery_shapes = (
        #                                     shape_id_periphery_orientation_0[0],
        #                                     shape_id_periphery_orientation_1[0],
        #                                     shape_id_periphery_orientation_2[0],
        #                                     shape_id_periphery_orientation_3[0],
        #                                     shape_id_periphery_orientation_4[0],
        #                                     shape_id_periphery_orientation_5[0],
        #                                     )
        #                                 periphery_orientation = (
        #                                     shape_id_periphery_orientation_0[1],
        #                                     shape_id_periphery_orientation_1[1],
        #                                     shape_id_periphery_orientation_2[1],
        #                                     shape_id_periphery_orientation_3[1],
        #                                     shape_id_periphery_orientation_4[1],
        #                                     shape_id_periphery_orientation_5[1],
        #                                     )
        #                                 if periphery_index not in periphery:
        #                                     periphery[periphery_index] = {}
        #                                 if periphery_shapes not in periphery[periphery_index]:
        #                                     periphery[periphery_index][periphery_shapes] = {}
        #                                 if periphery_orientation not in periphery[periphery_index][periphery_shapes]:
        #                                     periphery[periphery_index][periphery_shapes][periphery_orientation] = orientation
        # for periphery_index, periphery_shapes in sorted(periphery.items()):
        #     sys.stdout.write("{}: ".format(periphery_index))
        #     sys.stdout.write("{\n")
        #     for periphery_shape, periphery_orientations in periphery_shapes.items():
        #         sys.stdout.write("\t{}: ".format(periphery_shape))
        #         sys.stdout.write("{\n")
        #         for periphery_orientation, orientation in periphery_orientations.items():
        #             # axis_rotation, rotations = orientation
        #             sys.stdout.write("\t\t{}: {},\n".format(periphery_orientation, orientation))
        #         sys.stdout.write("\t},\n")
        #     sys.stdout.write("},\n")
        self.assertTrue(set(periphery_indxes.keys()).issubset(set(self.object.peripheries[shape_id_corner].keys())))

    def test_get_periphery_complex_hepta(self):
        shape_id_hepta = block_config.get_shape_id("hepta")
        smd = Smd()
        smd.read(self._blueprint[shape_id_hepta])
        self.object = Periphery(smd.get_block_list())
        annotation = Annotate(smd.get_block_list(), self.object)
        min_position, max_position = smd.get_min_max_vector()
        # marked, border = annotation.flood(min_position, min_position, max_position)
        annotation.calc_boundaries(min_position, max_position)
        marked, border = annotation.get_data()
        # block_list, marked, border
        self.object.set_annotation(marked=marked, border=border)
        periphery_indxes = {}
        for periphery_index, periphery_shape, periphery_orientation, orientation in self.object.get_periphery_complex(shape_id_hepta):
            if periphery_index not in periphery_indxes:
                periphery_indxes[periphery_index] = {}
        #     if orientation not in periphery_indxes[periphery_index]:
        #         periphery_indxes[periphery_index][orientation] = [set(), set(), set(), set(), set(), set()]
        #     for index, shape_id in enumerate(periphery_shape):
        #         periphery_indxes[periphery_index][orientation][index].add((shape_id, periphery_orientation[index]))
        #         # periphery_indxes[periphery_index][orientation][index][shape_id].add(periphery_orientation)
        #
        # periphery = {}
        # for periphery_index, orientations in sorted(periphery_indxes.items()):
        #     for orientation, periphery_vectors in orientations.items():
        #         for shape_id_periphery_orientation_0 in periphery_vectors[0]:
        #             for shape_id_periphery_orientation_1 in periphery_vectors[1]:
        #                 for shape_id_periphery_orientation_2 in periphery_vectors[2]:
        #                     for shape_id_periphery_orientation_3 in periphery_vectors[3]:
        #                         for shape_id_periphery_orientation_4 in periphery_vectors[4]:
        #                             for shape_id_periphery_orientation_5 in periphery_vectors[5]:
        #                                 periphery_shapes = (
        #                                     shape_id_periphery_orientation_0[0],
        #                                     shape_id_periphery_orientation_1[0],
        #                                     shape_id_periphery_orientation_2[0],
        #                                     shape_id_periphery_orientation_3[0],
        #                                     shape_id_periphery_orientation_4[0],
        #                                     shape_id_periphery_orientation_5[0],
        #                                     )
        #                                 periphery_orientation = (
        #                                     shape_id_periphery_orientation_0[1],
        #                                     shape_id_periphery_orientation_1[1],
        #                                     shape_id_periphery_orientation_2[1],
        #                                     shape_id_periphery_orientation_3[1],
        #                                     shape_id_periphery_orientation_4[1],
        #                                     shape_id_periphery_orientation_5[1],
        #                                     )
        #                                 if periphery_index not in periphery:
        #                                     periphery[periphery_index] = {}
        #                                 if periphery_shapes not in periphery[periphery_index]:
        #                                     periphery[periphery_index][periphery_shapes] = {}
        #                                 if periphery_orientation not in periphery[periphery_index][periphery_shapes]:
        #                                     periphery[periphery_index][periphery_shapes][periphery_orientation] = orientation
        # for periphery_index, periphery_shapes in sorted(periphery.items()):
        #     sys.stdout.write("{}: ".format(periphery_index))
        #     sys.stdout.write("{\n")
        #     for periphery_shape, periphery_orientations in periphery_shapes.items():
        #         sys.stdout.write("\t{}: ".format(periphery_shape))
        #         sys.stdout.write("{\n")
        #         for periphery_orientation, orientation in periphery_orientations.items():
        #             # axis_rotation, rotations = orientation
        #             sys.stdout.write("\t\t{}: {},\n".format(periphery_orientation, orientation))
        #         sys.stdout.write("\t},\n")
        #     sys.stdout.write("},\n")
        self.assertTrue(set(periphery_indxes.keys()).issubset(set(self.object.peripheries[shape_id_hepta].keys())))
