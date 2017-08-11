import unittest
import tempfile
import shutil
import os
import nose

from smlib.blueprint import Blueprint
from smlib.utils.blockconfig import block_config


__author__ = 'Sonny Lion'


class DefaultSetup(unittest.TestCase):
    """
    @type bp: Blueprint
    @type tmpdir: str
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.bp = None

    def setUp(self):
        # load block config
        block_config.from_hard_coded()

        # create tempdir
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        # clean the tmpdir
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)


class TestAddBlocks(DefaultSetup):
    """
    """

    def test_add_blocks(self):
        # create the blueprint and populate it
        self.bp = Blueprint("unittest_entity")
        # set the entity to space station
        self.bp.set_entity(2, 0)

        # define available rotations
        rotation_axes = {'+Y': 0b0,
                         '-Y': 0b1,
                         '-Z': 0b10,
                         '+Z': 0b11,
                         '-X': 0b100,
                         '+X': 0b101, }

        available_rotations = {axis_k: [(axis_v << 2) + step
                                        for step in [0, 1, 2, 3]]
                               for axis_k, axis_v in rotation_axes.items()}

        # create dict to store block properties
        data = dict()

        # define allowed rotations for each kind of blocks
        allowed_rotations_1 = ['+Y',  # wedge
                               '-Y',
                               '-Z',
                               '+Z', ]

        allowed_rotations_26 = ['+Y',  # corner/rail
                                '-Y',
                                '-Z',
                                '+Z',
                                '-X',
                                '+X', ]

        allowed_rotations_45 = ['+Y', '-Y', ]  # tetra/hepta

        # add blocks props to the properties dict

        # basic
        block_id_grey_hull = 598  # grey hull
        data[block_id_grey_hull] = {'positions': [(0, 0, 0)],
                                    'rotations': [0]}

        # wedge
        block_id_grey_hull_wedge = 599  # grey hull wedge
        wedge_rotation_list = [rotation for key in available_rotations
                               if key in allowed_rotations_1
                               for rotation in available_rotations[key]]
        data[block_id_grey_hull_wedge] = {'positions': [(1, 0, rotation)
                                                        for rotation in wedge_rotation_list],
                                          'rotations': wedge_rotation_list}

        # corner
        block_id_grey_hull_corner = 600  # grey hull corner
        corner_rotation_list = [rotation for key in available_rotations
                                if key in allowed_rotations_26
                                for rotation in available_rotations[key]]
        data[block_id_grey_hull_corner] = {'positions': [(2, 0, rotation)
                                                         for rotation in corner_rotation_list],
                                           'rotations': corner_rotation_list}

        # tetra/hepta
        block_id_grey_hull_tetra = 602  # grey hull tetra
        block_id_grey_hull_hepta = 601  # grey hull hepta
        tetra_rotation_list = [rotation for key in available_rotations
                               if key in allowed_rotations_45
                               for rotation in available_rotations[key]]
        data[block_id_grey_hull_tetra] = {'positions': [(3, 0, rotation)
                                                        for rotation in tetra_rotation_list],
                                          'rotations': tetra_rotation_list}

        data[block_id_grey_hull_hepta] = {'positions': [(3, 1, rotation)
                                                        for rotation in tetra_rotation_list],
                                          'rotations': tetra_rotation_list}

        # same with block facing
        block_facing_rotation = list(range(0, 6))
        block_id_grey_hull_slabe_34 = 700  # grey hull 3/4
        block_id_grey_hull_slabe_12 = 699  # grey hull 1/2
        block_id_grey_hull_slabe_14 = 698  # grey hull 1/4

        data[block_id_grey_hull_slabe_34] = {'positions': [(4, 0, rotation)
                                                           for rotation in block_facing_rotation],
                                             'rotations': block_facing_rotation}

        data[block_id_grey_hull_slabe_12] = {'positions': [(4, 1, rotation)
                                                           for rotation in block_facing_rotation],
                                             'rotations': block_facing_rotation}

        data[block_id_grey_hull_slabe_14] = {'positions': [(4, 2, rotation)
                                                           for rotation in block_facing_rotation],
                                             'rotations': block_facing_rotation}

        # finally add blocks to the bp
        for block_id in data:
            self.bp.add_blocks(block_id,
                               positions=data[block_id]['positions'],
                               rotations=data[block_id]['rotations'])

        # test the number of blocks added
        number_of_blocks = (1 +    # hull
                            4*4 +  # wedge - 4 axes * 4 rotations
                            6*4 +  # corner - 6 axes
                            2*4 +  # tetra - 2 axes
                            2*4 +  # hepta - 2 axes
                            6 +    # slab 3/4
                            6 +    # slab 1/2
                            6)     # slab 1/4
        self.assertEqual(number_of_blocks, self.bp.smd3.get_number_of_blocks())

        # test writing

        # write the data
        output = tempfile.mkdtemp(dir=self.tmpdir)
        self.bp.write(output)

        # delete the blueprint
        del self.bp


class TestRotatePosition(object):

    def test_rotate_position(self):
        # expected positions
        results = dict(x=[(1, 2, 3), (1, 3, -2), (1, -2, -3), (1, -3, 2)],
                       y=[(1, 2, 3), (-3, 2, 1), (-1, 2, -3), (3, 2, -1)],
                       z=[(1, 2, 3), (2, -1, 3), (-1, -2, 3), (-2, 1, 3)],)

        # loop over all possibilities
        for rotation_axis in ['x', 'y', 'z']:
            for rotation_number in range(0, 4):
                # use nose with generator to create multiple test cases
                # src: http://nose.readthedocs.io/en/latest/writing_tests.html
                yield self.check_position, (1, 2, 3), rotation_axis,\
                    rotation_number, results[rotation_axis][rotation_number]

    def check_position(self, position, rotation_axis, rotation_number, result):
        # compute position with given rotation axis/number
        new_position = tuple(Blueprint.rotate_position(position,
                                                       axis=rotation_axis,
                                                       number=rotation_number))
        assert new_position == result

if __name__ == '__main__':
    # run test using nose
    nose.core.runmodule()
