import unittest
import tempfile
import shutil

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
        block_config.from_hard_coded()
        # create the blueprint and populate it
        self.bp = Blueprint()

        # setup positions
        positions = [(14,  40,  17),
                     (7, -45, -47),
                     (-42, -47, -55),
                     (44,   8, -31),
                     (-2,  40,  15),
                     (-37,  45,  -8),
                     (-32, -11, -5),
                     (-18,  34, -36),
                     (-4,  37,  -9),
                     (37, -10,  23)]

        # sort positions
        positions.sort()

        # add blocks
        block_id_grey_hull = 598 # grey hull
        block_id_grey_hull_wedge = 599 # grey hull wedge
        block_id_grey_hull_corner = 600 # grey hull corner
        block_id_grey_hull_tetra = 602 # grey hull tetra
        block_id_grey_hull_hepta = 601 # grey hull hepta
        block_id_grey_hull_slabe_34 = 700 # grey hull 3/4
        block_id_grey_hull_slabe_12 = 699 # grey hull 1/2
        block_id_grey_hull_slabe_14 = 698 # grey hull 1/4
        self.bp.add_blocks(block_id_grey_hull, positions)
        self.bp.add_blocks(block_id_grey_hull_wedge, [(0, 0, 0)])
        self.bp.add_blocks(block_id_grey_hull_corner, [(0, 0, 1)])
        self.bp.add_blocks(block_id_grey_hull_tetra, [(0, 0, 2)])
        self.bp.add_blocks(block_id_grey_hull_hepta, [(0, 0, 3)])
        self.bp.add_blocks(block_id_grey_hull_slabe_34, [(0, 0, 4)])
        self.bp.add_blocks(block_id_grey_hull_slabe_12, [(0, 0, 5)])
        self.bp.add_blocks(block_id_grey_hull_slabe_14, [(0, 0, 6)])

        # set the entity to space station
        self.bp.set_entity(2, 0)

        self.bp.write('my_test_bp')

        # test the number of blocks added (all positions + ship core)
        self.assertEqual(len(positions), self.bp.smd3.get_number_of_blocks())

        # test the block position
        bp_positions = list(x for x in self.bp.smd3.get_block_list())
        bp_positions.sort()

        self.assertEqual(positions, bp_positions)

        # test writing

        # create tempdir
        self.tmpdir = tempfile.mkdtemp()
        # write the data
        self.bp.write(self.tmpdir)

    def tearDown(self):
        # delete the blueprint
        del self.bp

        # clean the tmpdir
        shutil.rmtree(self.tmpdir)


class TestAddBlocks(DefaultSetup):
    """
    """

    def test_positions(self):
        self.assertEqual(599, 599)
        # self.bp.get_block_list()

if __name__ == '__main__':
    unittest.main()