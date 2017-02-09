from lib.utils.blocklist import BlockList
from lib.utils.blockconfig import block_config
from lib.smblueprint.smdblock.blockhandler import block_handler


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

    _replace_cache_positive = dict()

    def replace_hull(self, new_hull_type, hull_type=None):
        """
        Replace all blocks of a specific hull type or all hull

        @param new_hull_type:
        @type new_hull_type: int
        @param hull_type:
        @type hull_type: int | None
        """
        for position, block in self._block_list.pop_positions():
            block_id = block.get_id()
            if not block_config[block_id].is_hull():
                self._block_list(position, block.get_int_24())
                continue
            if block_id not in self._replace_cache_positive:
                hull_tier, color_id, shape_id = block_config[block_id].get_details()
                if hull_tier is None:
                    self._block_list(position, block.get_int_24())
                    continue
                if hull_type is not None and hull_type != hull_tier:  # not replaced
                    self._block_list(position, block.get_int_24())
                    continue
                new_block_id = block_config.get_block_id_by_details(new_hull_type, color_id, shape_id)
                self._replace_cache_positive[block_id] = new_block_id
            new_block_id = self._replace_cache_positive[block_id]
            new_block_int = block_handler(new_block_id).get_modified_int_24bit(
                block_id=new_block_id, active=False, hit_points=block_config[new_block_id].hit_points)
            self._block_list(position, new_block_int)

    def replace_blocks(self, block_id, replace_id, compatible=False):
        """
        Replace all blocks of a specific id
        """
        for position, block in self._block_list.items():
            if block.get_id() != block_id:
                continue
            if compatible:
                new_int_24 = block.get_modified_int_24bit(block_id=replace_id)
            else:
                new_int_24 = block_handler(replace_id).get_modified_int_24bit(block_id=replace_id, active=False)
            self._block_list(position, new_int_24)
