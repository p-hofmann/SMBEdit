from lib.utils.blocklist import BlockList


__author__ = 'Peter Hofmann'


class Annotate(object):
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
            index = 0
            if position[index] < min_position[index]-1 or position[index] > max_position[index]+1:
                continue
            index = 1
            if position[index] < min_position[index]-1 or position[index] > max_position[index]+1:
                continue
            index = 2
            if position[index] < min_position[index]-1 or position[index] > max_position[index]+1:
                continue
            if self._block_list.has_block_at(position):
                border.add(position_index)
                continue

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
        return marked, border
