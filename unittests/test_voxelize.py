import unittest
import tempfile
import shutil
import os

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

    def test_mesh_vox(self):
        from voxlib.voxelize import voxelize
        # from mesh_vox.voxelizer import get_voxels as voxelize

        input_paths = [
            os.path.join(".", "input_mesh", "cube.stl"),
            os.path.join(".", "input_mesh", "cube_diagonals.stl"),
            os.path.join(".", "input_mesh", "cube_diagonals_axis.stl"),
            # os.path.join(".", "input_mesh", "Dragon_2_5.stl"),
            # os.path.join(".", "input_mesh", "Scaffold.obj"),
            ]
        resolution = 11

        for input_path in input_paths:
            # voxelize mesh
            self.assertTrue(os.path.exists(input_path), input_path)
            positions = set(voxelize(input_path, resolution=resolution))
            print(len(positions))

            # create blueprint and add blocks
            blueprint_name = os.path.splitext(os.path.basename(input_path))[0]
            self.bp.smd3.re = Blueprint(blueprint_name)
            # set the entity to space station
            self.bp.set_entity(2, 0)
            self.bp.add_blocks(
                598,
                positions=positions,
                offset=(16, 16, 16)
            )

            # create blueprint folder and save StarMade blueprint to it
            output_folder = self.tmpdir
            output_name = "test_{}_{}".format(blueprint_name, resolution)
            output = os.path.join(output_folder, output_name)
            if not os.path.exists(output):
                os.mkdir(output)
            self.bp.write(output)
            del self.bp


if __name__ == '__main__':
    unittest.main()
