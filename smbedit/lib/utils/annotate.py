from .blocklist import BlockList
from .periphery import PeripheryBase
from .vector import Vector


__author__ = 'Peter Hofmann'


class Annotate(object):
    """
    Collection of auto shape stuff

    @type _block_list: BlockList
    @type _periphery: PeripheryBase
    @type marked: set[int]
    @type border: set[int]
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
        del self._block_list
        self._block_list = None

    def get_data(self):
        """
        @rtype: (set(int), set(int))
        """
        return self.marked, self.border

    def remove_empty_voxel(self):
        for position_index in list(self.marked):
            position = Vector.get_position(position_index)
            if self._periphery.get_position_block_periphery_index(position, 3) == 0:
                self.marked.remove(position_index)

    def _add_neighbours_to_query(self, query, position):
        for taxi_dist, position_tmp in self.get_neighbours(position):
            if taxi_dist == 3:
                continue
            position_index_tmp = Vector.get_index(position_tmp)
            if taxi_dist == 2:
                if self._block_list.has_block_at(position_tmp):
                    self.border.add(position_index_tmp)
                continue
            if position_index_tmp in self.marked:
                continue
            if position_index_tmp in self.border:
                continue
            query.add(position_index_tmp)

    def flood(self, start_position, min_position, max_position):
        """

        @type start_position: (int, int, int)
        @type min_position: (int, int, int)
        @type max_position: (int, int, int)

        @rtype: None
        """
        self.marked = set()
        self.border = set()
        tmp = set()
        assert not self._block_list.has_block_at(start_position), "Start Position must be empty."
        tmp.add(Vector.get_index(start_position))
        while len(tmp) > 0:
            position_index = tmp.pop()
            position = Vector.get_position(position_index)
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
                self.border.add(position_index)
                continue
            self.marked.add(position_index)
            self._add_neighbours_to_query(tmp, position)

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

    def trace_boundary(self, start_position):
        """

        @type start_position: (int, int, int)

        @rtype: None
        """
        assert self._periphery.get_position_block_periphery_index(start_position) > 0
        tmp = set()
        tmp.add(Vector.get_index(start_position))
        while len(tmp) > 0:
            position_index = tmp.pop()
            position = Vector.get_position(position_index)
            if self._block_list.has_block_at(position):
                self.border.add(position_index)
                continue
            if self._periphery.get_position_block_periphery_index(position, 3) == 0:
                continue
            self.marked.add(position_index)
            self._add_neighbours_to_query(tmp, position)

    def calc_boundaries(self, min_position, max_position):
        """

        @type min_position: (int, int, int)
        @type max_position: (int, int, int)

        @rtype: None
        """
        self.marked = set()
        self.border = set()
        min_position = Vector.subtraction(min_position, (1, 1, 1))
        max_position = Vector.addition(max_position, (1, 1, 1))
        for x in range(min_position[0], max_position[0]):
            for y in range(min_position[1], max_position[1]):
                for z in range(min_position[2], max_position[2]):
                    position = (x, y, z)
                    if self._periphery.get_position_block_periphery_index(position) == 0:
                        continue
                    self.trace_boundary(position)
                    return
