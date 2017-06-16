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

        block_id = 598 # Grey Hull
        self.bp.add_blocks(block_id, positions)

        # set the entity to ship
        self.bp.set_entity(0, 0)

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