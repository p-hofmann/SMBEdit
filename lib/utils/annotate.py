from lib.utils.blocklist import BlockList
from lib.utils.periphery import PeripheryBase


__author__ = 'Peter Hofmann'


class Annotate(object):
    """
    Collection of auto shape stuff

    @type _block_list: BlockList
    @type _periphery: PeripheryBase
    @type marked: set[str]
    @type border: set[str]
    """

    def __init__(self, block_list, periphery):
        """

        @type block_list: BlockList
        """
        self._block_list = block_list
        self._periphery = periphery
        self.marked = set()
        self.border = set()

    def __del__(self):
        list = self._block_list
        self._block_list = None
        del list

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

    @staticmethod
    def get_neighbours(position):
        range_p = [-1, 0, 1]
        for x in range_p:
            for y in range_p:
                for z in range_p:
                    taxi_dist = abs(x) + abs(y) + abs(z)
                    position_tmp = (position[0] + x, position[1] + y, position[2] + z)
                    if position_tmp == position:
                        continue
                    yield taxi_dist, position_tmp

    def trace_boundary(self, start_position, min_position, max_position):
        assert self._periphery.get_position_block_periphery_index(start_position) > 0
        tmp = set()
        tmp.add(self._block_list.get_index(start_position))
        while len(tmp) > 0:
            position_index = tmp.pop()
            position = self._block_list.get_position(position_index)
            if self._block_list.has_block_at(position):
                self.border.add(position_index)
                continue
            if self._periphery.get_position_block_periphery_index(position, 3) == 0:
                continue
            for index in range(3):
                if position[index] < min_position[index]-1 or position[index] > max_position[index]+1:
                    continue
            self.marked.add(position_index)

            for taxi_dist, position_tmp in self.get_neighbours(position):
                if taxi_dist == 3:
                    continue
                position_index = self._block_list.get_index(position_tmp)
                if taxi_dist == 2 and self._block_list.has_block_at(position_tmp):
                    self.border.add(position_index)
                if taxi_dist == 1:
                    if position_index not in self.marked and position_index not in self.border:
                        tmp.add(position_index)

    def get_boundaries(self, min_position, max_position):
        outside = True
        for x in range(min_position[0], max_position[0]+1):
            for y in range(min_position[1], max_position[1]+1):
                for z in range(min_position[2], max_position[2]+1):
                    position = (x, y, z)
                    if self._periphery.get_position_block_periphery_index(position) == 0:
                        continue
                    if self._block_list.has_block_at(position):
                        outside = False
                        continue
                    position_index = self._block_list.get_index(position)
                    if position_index in self.marked:
                        outside = True
                    if not outside:
                        continue
                    self.trace_boundary(position, min_position, max_position)
                    return self.marked, self.border
