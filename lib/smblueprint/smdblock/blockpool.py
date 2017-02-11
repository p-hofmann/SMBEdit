__author__ = 'Peter Hofmann'

from weakref import WeakValueDictionary
from lib.utils.blockconfig import block_config
from lib.smblueprint.smdblock.style.stylebasic import StyleBasic
from lib.smblueprint.smdblock.style.style0 import Style0
from lib.smblueprint.smdblock.style.style1wedge import Style1Wedge
from lib.smblueprint.smdblock.style.style2corner import Style2Corner
from lib.smblueprint.smdblock.style.style3 import Style3
from lib.smblueprint.smdblock.style.style4tetra import Style4Tetra
from lib.smblueprint.smdblock.style.style5hepta import Style5Hepta
from lib.smblueprint.smdblock.style.style6 import Style6


class BlockPool(object):
    """
    @type _state_to_instance: WeakValueDictionary[int, Block]
    """

    _state_to_instance = WeakValueDictionary()

    _valid_versions = {0, 1, 2, 3}

    def __init__(self):
        self._basic = StyleBasic(0, 0)
        self._styles = [Style0, Style1Wedge, Style2Corner, Style3, Style4Tetra, Style5Hepta, Style6]
        self._max_version = max(BlockPool._valid_versions)

    def __call__(self, state, version=None):
        """
        @param state:
        @type state: int
        @param version: version of smd segment
        @type version: int

        @rtype: Block | None
        """
        max_version = self.get_max_version()
        if version is None:
            version = max_version
        block = self.get_block(state, version)
        if block is None:
            return None
        if version < max_version:
            block.convert(max_version)
        # check if this block state already exist
        instance_pool = self._state_to_instance.get(block.get_int_24())
        if not instance_pool:
            instance_pool = block
            self._state_to_instance[state] = instance_pool
        return instance_pool

    # Methods, called on instance objects:
    def __iter__(self):
        """
        @rtype: Iterable[Block]
        """
        return iter(self._state_to_instance.values())

    def __getitem__(self, state):
        """
        Get a block at a specific position

        @param state:
        @type state: int

        @rtype: Block
        """
        assert state in self._state_to_instance, "No block for state: {}".format(state)
        return self._state_to_instance[state]

    def __len__(self):
        """
        Get number of blocks of blueprint

        @return: number of blocks in segment
        @rtype: int
        """
        return len(self._state_to_instance)

    def get_max_version(self):
        return self._max_version

    def get_block(self, int_24bit, version=None):
        """

        @type int_24bit: int

        @rtype: StyleBasic | None
        """
        if version is None:
            version = self._max_version
        self._basic(int_24bit, version)
        if self._basic.get_id() == 0:
            return None
        block_style = block_config[self._basic.get_id()].block_style
        return self._styles[block_style](int_24bit, version)

    @staticmethod
    def items():
        """
        @rtype: Iterable[(int, Block)]
        """
        return BlockPool._state_to_instance.items()

    @staticmethod
    def popitem():
        """
        @rtype: Iterable[(int, int, int), Block]
        """
        state_pool = BlockPool._state_to_instance
        BlockPool._state_to_instance = dict()
        for state, block in state_pool.popitem():
            yield state, block

block_pool = BlockPool()
