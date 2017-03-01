from lib.utils.blocklist import BlockList
from lib.utils.blockconfig import block_config
from lib.smblueprint.smdblock.blockpool import block_pool


__author__ = 'Peter Hofmann'


class Replace(object):
    """
    Collection of auto shape stuff

    @type _block_list: BlockList
    """

    def __init__(self, block_list):
        """

        @type block_list: BlockList
        """
        self._block_list = block_list

    def replace_hull(self, new_hull_type, hull_type=None):
        """
        Replace all blocks of a specific hull type or all hull

        @param new_hull_type:
        @type new_hull_type: int
        @param hull_type:
        @type hull_type: int | None
        """
        replace_cache_positive = dict()
        for position, block in self._block_list.pop_positions():
            block_id = block.get_id()
            if not block_config[block_id].is_hull():
                self._block_list[position] = block
                continue
            if block_id not in replace_cache_positive:
                hull_tier, color_id, shape_id = block_config[block_id].get_details()
                if hull_tier is None:
                    self._block_list[position] = block
                    continue
                if hull_type is not None and hull_type != hull_tier:  # not replaced
                    self._block_list[position] = block
                    continue
                new_block_id = block_config.get_block_id_by_details(new_hull_type, color_id, shape_id)
                replace_cache_positive[block_id] = new_block_id
            new_block_id = replace_cache_positive[block_id]
            new_block = block_pool(new_block_id).get_modified_block(
                block_id=new_block_id, active=False,
                block_side_id=block.get_block_side_id(), axis_rotation=block.get_axis_rotation(),
                rotations=block.get_rotations())
            self._block_list[position] = new_block

    def replace_blocks(self, block_id, replace_id, compatible=False):
        """
        Replace all blocks of a specific id
        """
        for position, block in self._block_list.items():
            if block.get_id() != block_id:
                continue
            if compatible:
                new_block = block.get_modified_block(block_id=replace_id)
            else:
                new_block = block_pool(replace_id).get_modified_block(
                    block_id=replace_id, active=False)
            self._block_list[position] = new_block

    def reset_hull_shape(self, border):
        """
        Turn shape of armor blocks of ship hull to cubes

        @param border: Set of position_index of blocks
        @type border: set(int)
        """
        cube_id = block_config.get_shape_id('cube')
        for position_index in border:
            block = self._block_list[position_index]
            block_id = block.get_id()
            if not block_config[block_id].is_hull():
                continue
            if block_config[block.get_id()].shape == cube_id:
                continue
            block_hull_tier, color_id, _ = block_config[block_id].get_details()
            new_block_id = block_config.get_block_id_by_details(
                hull_type=block_hull_tier, color=color_id, shape_id=cube_id)
            new_block = block.get_modified_block(block_id=new_block_id, block_side_id=0)
            self._block_list[position_index] = new_block
