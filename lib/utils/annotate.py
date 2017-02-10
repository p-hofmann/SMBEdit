import sys
from lib.utils.blocklist import BlockList
from lib.utils.blockconfig import block_config
from lib.smblueprint.smdblock.blockhandler import block_handler


__author__ = 'Peter Hofmann'


class AutoShape(object):
    """
    Collection of auto shape stuff

    @type _block_list: BlockList
    """

    def __init__(self, block_list):
        """

        @type block_list: BlockList
        """
        self._block_list = block_list

    def flood(self, start_position, min_position, max_position, margin=0):
        marked = set()
        border = set()
        tmp = set()
        assert not self._block_list.has_block_at(start_position), "Start Position must be empty."
        tmp.add(self._block_list.get_index(start_position))
        while len(tmp) > 0:
            position_index = tmp.pop()
            position = self._block_list.get_position(position_index)
            if min_position >= position or max_position <= position:
                continue
            if self._block_list.has_block_at(position):
                border.add(position_index)
            else:
                marked.add(position_index)
                position_index = self._block_list.get_index((position[0]-1, position[1], position[2]))
                if position_index not in marked and position_index not in border:
                    tmp.add(position_index)
                position_index = self._block_list.get_index((position[0], position[1]-1, position[2]))
                if position_index not in marked and position_index not in border:
                    tmp.add(position_index)
                position_index = self._block_list.get_index((position[0], position[1], position[2]-1))
                if position_index not in marked and position_index not in border:
                    tmp.add(position_index)
                position_index = self._block_list.get_index((position[0]+1, position[1], position[2]))
                if position_index not in marked and position_index not in border:
                    tmp.add(position_index)
                position_index = self._block_list.get_index((position[0], position[1]+1, position[2]))
                if position_index not in marked and position_index not in border:
                    tmp.add(position_index)
                position_index = self._block_list.get_index((position[0], position[1], position[2]+1))
                if position_index not in marked and position_index not in border:
                    tmp.add(position_index)
