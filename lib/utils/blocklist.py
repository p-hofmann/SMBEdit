from collections import Iterable
import struct
from lib.smblueprint.smdblock.blockpool import StyleBasic


class BlockList(object):
    """
    @type _position_index_to_instance: dict[bytes | str, StyleBasic]
    """

    def __init__(self):
        self._position_index_to_instance = dict()

    # Methods, called on class objects:
    def __iter__(self):
        """
        @rtype: Iterable[(int, int, int)]
        """
        for position_index in self._position_index_to_instance:
            yield self.get_position(position_index)

    def items(self):
        """
        @rtype: Iterable[((int, int, int), StyleBasic)]
        """
        for position_index in self._position_index_to_instance:
            yield self.get_position(position_index), self._position_index_to_instance[position_index]

    def __setitem__(self, position, block):
        """
        @param position:
        @type position: (int, int, int)
        @param block:
        @type block: StyleBasic
        """
        assert isinstance(block, StyleBasic), block
        position_index = self.get_index(position)
        self._position_index_to_instance[position_index] = block

    def __getitem__(self, position):
        """
        Get a block at a specific position

        @param position:
        @type position: (int, int, int) | bytes | str

        @rtype: StyleBasic
        """
        if isinstance(position, (bytes, str)):
            position_index = position
        else:
            position_index = self.get_index(position)
        assert position_index in self._position_index_to_instance, "{} No block at position: {}".format(len(self), position)
        return self._position_index_to_instance[position_index]

    def __len__(self):
        """
        Get number of blocks of blueprint

        @return: number of blocks in segment
        @rtype: int
        """
        return len(self._position_index_to_instance)

    def pop_positions(self):
        """
        @rtype: Iterable[(int, int, int), StyleBasic]
        """
        blocks = self._position_index_to_instance
        self._position_index_to_instance = dict()
        while len(blocks) > 0:
            position_index, block = blocks.popitem()
            yield self.get_position(position_index), block

    def pop_position_indexes(self):
        """
        @rtype: Iterable[bytes | str, StyleBasic]
        """
        blocks = self._position_index_to_instance
        self._position_index_to_instance = dict()
        while len(blocks) > 0:
            position_index, block = blocks.popitem()
            yield position_index, block

    def pop(self, position):
        """
        Remove Block at specific position.

        @param position: x,z,y position of a block
        @type position: (int, int, int)

        @rtype: StyleBasic
        """
        assert isinstance(position, tuple)
        assert self.has_block_at(position), "No block at position: {}".format(position)
        return self._position_index_to_instance.pop(self.get_index(position))

    def keys(self):
        """
        @rtype: Iterable[int]
        """
        for position_index in self._position_index_to_instance:
            yield position_index

    # #######################################
    # ###  Position - Index
    # #######################################

    @staticmethod
    def get_index(position):
        """

        @param position:
        @type position: (int, int, int)

        @rtype: bytes | str
        """
        return struct.pack("hhh", position[0], position[1], position[2])

    @staticmethod
    def get_position(position_index):
        """

        @param position_index:
        @type position_index: bytes | str

        @rtype: (int, int, int)
        """
        return struct.unpack("hhh", position_index)

    def _shift_index(self, position_index, offset_x, offset_y, offset_z):
        """

        @type position_index: bytes | str
        @type offset_x: int
        @type offset_y: int
        @type offset_z: int

        @return:
        @rtype: bytes | str
        """
        position = self.get_position(position_index)
        new_position = [position[0]+offset_x, position[1]+offset_y, position[2]+offset_z]
        return self.get_index(tuple(new_position))

    # #######################################
    # ###  Get
    # #######################################

    def has_block_at(self, position):
        """
        Returns true if a block exists at a position

        @param position: (x,y,z)
        @type position: (int, int, int)

        @return:
        @rtype: bool
        """
        return self.get_index(position) in self._position_index_to_instance

    def has_core(self, position_core=(16, 16, 16)):
        if self.has_block_at(position_core) and self[position_core].get_id() == 1:
            return True
        return False

    def remove_blocks(self, block_ids):
        """
        Removing all blocks of a specific id

        @param block_ids:
        @type block_ids: set[int]
        """
        del_position_indexes = self.search_all(block_ids)   # should be smaller than making a list of '.keys()'
        for position_index in del_position_indexes:
            self._position_index_to_instance.pop(position_index)

    def search_all(self, block_ids):
        """
        Search and return the global position of block positions

        @param block_ids: Block id as found in utils class
        @type block_ids: set[int]

        @return: set of (x,y,z)
        @rtype: set[bytes | str]
        """
        position_indexes = set()
        for position_index in self._position_index_to_instance:
            if self[position_index].get_id() not in block_ids:
                continue
            position_indexes.add(position_index)
        return position_indexes

    def search_positions(self, block_ids):
        """
        Search and return the global position of block positions

        @param block_ids: Block id as found in utils class
        @type block_ids: set[int]

        @return: set of (x,y,z)
        @rtype: set[int]
        """
        position_indexes = set()
        for position_index in self._position_index_to_instance:
            if self[position_index].get_id() not in block_ids:
                continue
            position_indexes.add(position_index)
        return position_indexes

    def search(self, block_id):
        """
        Search and return the global position of the first occurrence of a block
        If no block is found, return None

        @param block_id: Block id as found in utils class
        @type block_id: int

        @return: None or (x,y,z)
        @rtype: None | tuple[int]
        """
        for position_index in self._position_index_to_instance:
            if self[position_index].get_id() == block_id:
                return self.get_position(position_index)
        return None

    def move_positions(self, vector_direction):
        """
        Move all positions in a direction

        @type vector_direction: (int, int, int)
        """
        for position_index, block in self.pop_position_indexes():
            new_position_index = self._shift_index(
                position_index, vector_direction[0], vector_direction[1], vector_direction[2])
            self._position_index_to_instance[new_position_index] = block
