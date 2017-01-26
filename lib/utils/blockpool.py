from collections import Iterable
from weakref import WeakValueDictionary
from lib.smblueprint.smd3.smdblock.block import Block


class BlockPool(object):
    """
    @type _state_to_instance: WeakValueDictionary[int, Block]
    @type _position_to_instance: dict[tuple[int], Block]
    """

    def __init__(self):
        self._state_to_instance = WeakValueDictionary()
        self._position_to_instance = dict()

    def __call__(self, position, state):
        """
        @param position:
        @type position: tuple[int]
        @param state:
        @type state: int

        @rtype: Block
        """
        return self._get_block_instance(position, state)

    # Methods, called on class objects:
    def __iter__(self):
        """
        @rtype: Iterable[Block]
        """
        return iter(self._state_to_instance.values())

    def items(self):
        """
        @rtype: Iterable[(tuple[int], Block)]
        """
        return self._position_to_instance.items()
    
    def __getitem__(self, position):
        """
        Get a block at a specific position

        @param position:
        @type position: tuple[int]

        @rtype: Block
        """
        assert position in self._position_to_instance, "No block at position: {}".format(position)
        return self._position_to_instance[position]

    def __len__(self):
        """
        Get number of blocks of blueprint

        @return: number of blocks in segment
        @rtype: int
        """
        return len(self._position_to_instance)

    # #######################################
    # ###  Get
    # #######################################

    def _get_block_instance(self, position, state):
        """
        @param position:
        @type position: tuple[int]
        @param state:
        @type state: int

        @rtype: Block
        """
        instance_pool = self._state_to_instance.get(state)

        # check if this block state already exist
        if not instance_pool:
            instance_pool = Block(state)
            self._state_to_instance[state] = instance_pool

        # check if this position contain already a block state and if it's the same
        instance_position = self._position_to_instance.get(position)
        if instance_position is not instance_pool:
            self._position_to_instance[position] = instance_pool

        return instance_pool

    def has_block_at(self, position):
        """
        Returns true if a block exists at a position

        @param position: (x,y,z)
        @type position: tuple[int]

        @return:
        @rtype: bool
        """
        return position in self._position_to_instance

    def remove_block(self, position):
        """
        Remove Block at specific position.

        @param position: x,z,y position of a block
        @type position: tuple[int]
        """
        assert isinstance(position, tuple)
        assert self.has_block_at(position), "No block at position: {}".format(position)
        self._position_to_instance.pop(position)
