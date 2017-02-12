from lib.utils.blocklist import BlockList
from lib.utils.blockconfig import block_config
from lib.utils.periphery import PeripheryBase
from lib.smblueprint.smdblock.blockpool import block_pool


__author__ = 'Peter Hofmann'


class AutoShape(object):
    """
    Collection of auto shape stuff

    @type _block_list: BlockList
    @type _periphery: PeripheryBase
    """

    def __init__(self, block_list, periphery):
        """

        @type block_list: BlockList
        @type periphery: PeripheryBase
        """
        self._block_list = block_list
        self._periphery = periphery

    def auto_hull_shape_independent(self, auto_wedge, auto_tetra):
        """
        Replace hull blocks with shaped hull blocks with shapes,
        that can be determined without knowing the shapes of blocks around it

        @type auto_wedge: bool
        @type auto_tetra: bool
        """
        for position, block in self._block_list.items():
            block_id = block.get_id()
            if not block_config[block_id].is_hull():
                continue
            orientation_simple = self._periphery.get_orientation_simple(
                position, shape_wedge=auto_wedge, shape_tetra=auto_tetra)
            if orientation_simple is None:
                continue
            new_shape_id, [axis_rotation, rotations] = orientation_simple
            block_hull_tier, color_id, shape_id = block_config[block_id].get_details()
            new_block_id = block_config.get_block_id_by_details(block_hull_tier, color_id, new_shape_id)
            new_block = block_pool(new_block_id).get_modified_block(
                block_id=new_block_id, axis_rotation=axis_rotation, rotations=rotations)
            self._block_list[position] = new_block

    def auto_hull_shape_dependent(self, block_shape_id):
        """
        Replace hull blocks with shaped hull blocks with shapes,
        that can only be determined by the shapes of blocks around it

        @type block_shape_id: int
        """
        for position, block in self._block_list.items():
            block_id = block.get_id()
            if not block_config[block_id].is_hull():
                continue
            orientation_complex = self._periphery.get_orientation_complex(position, block_shape_id)
            if orientation_complex is None:
                continue
            axis_rotation, rotations = orientation_complex
            block_hull_type, color, shape_id = block_config[block_id].get_details()
            new_block_id = block_config.get_block_id_by_details(block_hull_type, color, block_shape_id)
            new_block = block_pool(new_block_id).get_modified_block(
                block_id=new_block_id, axis_rotation=axis_rotation, rotations=rotations)
            self._block_list[position] = new_block

    def auto_hull_shape(self, auto_wedge, auto_tetra, auto_corner, auto_hepta=None):
        """
        Automatically set shapes to blocks on edges and corners.

        @type auto_wedge: bool
        @type auto_tetra: bool
        @type auto_corner: bool
        @type auto_hepta: bool
        """
        self.auto_hull_shape_independent(auto_wedge, auto_tetra)
        shape_id_corner = block_config.get_shape_id("corner")
        shape_id_hepta = block_config.get_shape_id("hepta")
        if auto_corner:
            self.auto_hull_shape_dependent(shape_id_corner)
        if auto_hepta:
            self.auto_hull_shape_dependent(shape_id_hepta)
