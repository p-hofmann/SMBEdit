from collections import Iterable

from lib.smblueprint.smdblock.block import BlockSmd3


class BlockList(object):
    """
    @type _position_index_to_instance: dict[int, BlockSmd3]
    """

    def __init__(self):
        self._position_index_to_instance = dict()

    def __call__(self, position, block):
        """
        @param position:
        @type position: (int, int, int)
        @param block:
        @type block: BlockSmd3

        @rtype: BlockSmd3
        """
        position_index = self.get_index(position)

        # check if this position contain already a block state and if it's the same
        instance_position = self._position_index_to_instance.get(position_index)
        if instance_position is not block:
            self._position_index_to_instance[position_index] = block

    # Methods, called on class objects:
    def __iter__(self):
        """
        @rtype: Iterable[(int, int, int)]
        """
        for position_index in self._position_index_to_instance:
            yield self._get_position(position_index)

    def items(self):
        """
        @rtype: Iterable[((int, int, int), BlockSmd3)]
        """
        for position_index in self._position_index_to_instance:
            yield self._get_position(position_index), self._position_index_to_instance[position_index]
    
    def __getitem__(self, position):
        """
        Get a block at a specific position

        @param position:
        @type position: (int, int, int)

        @rtype: BlockSmd3
        """
        position_index = self.get_index(position)
        assert position_index in self._position_index_to_instance, "No block at position: {}".format(position)
        return self._position_index_to_instance[position_index]

    def __len__(self):
        """
        Get number of blocks of blueprint

        @return: number of blocks in segment
        @rtype: int
        """
        return len(self._position_index_to_instance)

    def popitem(self):
        """
        @rtype: Iterable[(int, int, int), BlockSmd3]
        """
        blocks = self._position_index_to_instance
        self._position_index_to_instance = dict()
        while len(blocks) > 0:
            position_index, block = blocks.popitem()
            yield self._get_position(position_index), block

    def pop(self, position):
        """
        Remove Block at specific position.

        @param position: x,z,y position of a block
        @type position: (int, int, int)

        @rtype: BlockSmd3
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

        @rtype: int
        """
        return int(position[2] << 32) + int(position[1] << 16) + int(position[0])

    def _get_position(self, position_index):
        """

        @param position_index:
        @type position_index: int, int, int

        @rtype: int
        """
        return self._get_pos(position_index), self._get_pos(position_index, 16), self._get_pos(position_index, 32)

    @staticmethod
    def _get_pos(position_index, shift=0):
        """

        @param position_index:
        @type position_index: int

        @return:
        @rtype: int
        """
        if shift == 0:
            return int(position_index & 65535)
        return int(position_index >> shift & 65535)

    def _shift_index(self, position_index, offset_x, offset_y, offset_z):
        """

        @type position_index: int
        @type offset_x: int
        @type offset_y: int
        @type offset_z: int

        @return:
        @rtype: int
        """
        return self.get_index((
            self._get_pos(position_index) + offset_x,
            self._get_pos(position_index, 16) + offset_y,
            self._get_pos(position_index, 32) + offset_z))

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
        @rtype: set[int]
        """
        position_indexes = set()
        for position_index in self._position_index_to_instance:
            if self._position_index_to_instance[position_index].get_id() not in block_ids:
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
            if self._position_index_to_instance[position_index].get_id() not in block_ids:
                continue
            position_indexes.add(position_index)
        return position_indexes

    def search(self, block_id):
        """
        Search and return the global position of the first occurance of a block
        If no block is found, return None

        @param block_id: Block id as found in utils class
        @type block_id: int

        @return: None or (x,y,z)
        @rtype: None | tuple[int]
        """
        for position_index in self._position_index_to_instance:
            if self._position_index_to_instance[position_index].get_id() == block_id:
                return self._get_position(position_index)
        return None

    def move_positions(self, vector_direction):
        """
        Move all positions in a direction

        @type vector_direction: (int, int, int)
        """
        new_position_index_to_instance = dict()
        for position_index in self._position_index_to_instance:
            block = self._position_index_to_instance.pop(position_index)
            new_position_index = self._shift_index(
                position_index, vector_direction[0], vector_direction[1], vector_direction[2])
            new_position_index_to_instance[new_position_index] = block
