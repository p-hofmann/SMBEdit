__author__ = 'Peter Hofmann'

import sys
from collections import Iterable
from weakref import WeakValueDictionary

from lib.bits_and_bytes import BitAndBytes
from lib.utils.blockconfig import block_config
from lib.smblueprint.smdblock.style0 import Style0
from lib.smblueprint.smdblock.style1wedge import Style1Wedge
from lib.smblueprint.smdblock.style2corner import Style2Corner
from lib.smblueprint.smdblock.style3 import Style3
from lib.smblueprint.smdblock.style4tetra import Style4Tetra
from lib.smblueprint.smdblock.style5hepta import Style5Hepta
from lib.smblueprint.smdblock.style6 import Style6


class BlockPool(object):
    """
    @type _state_to_instance: WeakValueDictionary[int, Block]
    """

    _state_to_instance = WeakValueDictionary()

    def __call__(self, state, segment_version=3):
        """
        @param state:
        @type state: int
        @param segment_version: version of smd segment
        @type segment_version: int

        @rtype: Block
        """
        if segment_version < 2:
            return BlockV1(state).to_v3()
        if segment_version == 2:
            return BlockV2(state).to_v3()
        # check if this block state already exist
        instance_pool = self._state_to_instance.get(state)
        if not instance_pool:
            instance_pool = BlockV3(state)
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


class Block(object):

    def __init__(self, int_24bit=0):
        self._int_24bit = int_24bit

        self._bit_block_id_start = 0
        self._bit_block_id_length = 0

        self._bit_hit_points_start = 0
        self._bit_hit_points_length = 0

        self._bit_is_active_start = 0
        self._bit_is_active_length = 0

    def __repr__(self):
        return "{}".format(block_config[self.get_id()].name)

    def __eq__(self, other):
        return self._int_24bit == other.get_int_24bit    # Get

    def get_id(self):
        """
        Returns the block id

        @rtype: int
        """
        return BitAndBytes.bits_parse(self._int_24bit, self._bit_block_id_start, self._bit_block_id_length)

    def get_hit_points(self):
        """
        Returns the hit points of the block

        @rtype: int
        """
        assert self.get_id() != 0, "Block id 0 has no hit points."
        return BitAndBytes.bits_parse(self._int_24bit, self._bit_hit_points_start, self._bit_hit_points_length)

    def get_style(self):
        """
        Returns the block style

        @rtype: int | None
        """
        block_id = self.get_id()
        assert block_id != 0
        return block_config[block_id].block_style

    def is_active(self):
        """
        Returns the 'active' status.

        @rtype: bool
        """
        if not block_config[self.get_id()].can_activate:
            return False
        return self._get_active_value() == 0

    def _get_active_value(self):
        """
        Returns the 'active' bit value.

        @rtype: bool
        """
        return BitAndBytes.bits_parse(self._int_24bit, self._bit_is_active_start, self._bit_is_active_length)

    def get_orientation(self, style=None):
        if style is None:
            style = self.get_style()
        if style == 0:
            return Style0(self._int_24bit)
        if style == 1:
            return Style1Wedge(self._int_24bit)
        if style == 2:
            return Style2Corner(self._int_24bit)
        if style == 3:
            return Style3(self._int_24bit)
        if style == 4:
            return Style4Tetra(self._int_24bit)
        if style == 5:
            return Style5Hepta(self._int_24bit)
        if style == 6:
            return Style6(self._int_24bit)

    def get_int_24bit(self):
        """
        Get integer representing block

        @rtype int_24bit: int
        """
        return self._int_24bit

    def get_converted_to_type_6(self, block_id):
        """
        Return a side to type 6 orientation conversion, focusing on forward and up

        @type block_id: int

        @rtype: Block
        """
        assert self.get_style() == 0
        assert block_config[block_id].block_style == 6
        orientation = Style0(self._int_24bit)
        bit_19, bit_23, bit_22, rotations = orientation.to_style6_bits()
        hit_points = block_config[block_id].hit_points
        return self.get_modification(
            block_id=block_id, hit_points=hit_points, active=False,
            bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)

    def get_modification(self, block_id=None, hit_points=None, active=None, block_side_id=None, bit_19=None, bit_22=None, bit_23=None, rotations=None):
        """
        In the rare case a block value is changed, they are turned into a byte string.

        @type block_id: int | None
        @type hit_points: int | None
        @type active: bool | None

        @rtype: Block
        """
        if block_id is None:
            block_id = self.get_id()
        elif block_id == 0:
            self._int_24bit = 0
            return
        elif hit_points is None:
            hit_points = block_config[block_id].hit_points

        if hit_points is None:
            hit_points = self.get_hit_points()

        if active is None:
            active = self._get_active_value()
        elif active:
            active = 0
        elif not active:
            active = 1

        style = block_config[block_id].block_style
        int_24bit = 0
        int_24bit = BitAndBytes.bits_combine(block_id, int_24bit, 0)
        int_24bit = BitAndBytes.bits_combine(hit_points, int_24bit, self._bit_hit_points_start)
        if block_config[self.get_id()].can_activate:  # For blocks with an activation status
            int_24bit = BitAndBytes.bits_combine(active, int_24bit, self._bit_is_active_start)
        orientation = self.get_orientation(style)
        int_24bit = orientation.bit_combine(
            int_24bit, style=style, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23,
            rotations=rotations, block_side_id=block_side_id)
        return block_pool(int_24bit)

    def get_mirror(self, axis_index):
        """
        Mirror orientation
        @type axis_index: int

        @rtype: Block
        """
        orientation = self.get_orientation()
        if axis_index == 0:
            orientation.mirror_x()
        if axis_index == 1:
            orientation.mirror_y()
        if axis_index == 2:
            orientation.mirror_z()
        int_24bit = orientation.bit_combine(self._int_24bit)
        return block_pool(int_24bit)

    # #######################################
    # ###  Stream
    # #######################################

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream block values

        @param output_stream:
        @type output_stream: fileIO
        """
        output_stream.write("({})\t".format(self.get_style()))
        output_stream.write("HP: {}\t".format(self.get_hit_points()))
        output_stream.write("Active: {}\t".format(self.is_active()))
        orientation = self.get_orientation()
        output_stream.write("Or.: {}\t".format(orientation.to_string()))
        output_stream.write("{}\n".format(block_config[self.get_id()].name))

    def to_v2(self):
        block_id = self.get_id()
        active = self._get_active_value()
        bit_19, bit_23, bit_22, rotations = self.get_orientation().get_orientation_values()
        block_side_id = self.get_orientation().get_block_side_id()
        return BlockV2(self._int_24bit).get_modification(
            block_id=block_id, active=active,
            block_side_id=block_side_id, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)

    def to_v3(self):
        block_id = self.get_id()
        active = self._get_active_value()
        bit_19, bit_23, bit_22, rotations = self.get_orientation().get_orientation_values()
        block_side_id = self.get_orientation().get_block_side_id()
        return BlockV3(self._int_24bit).get_modification(
            block_id=block_id, active=active,
            block_side_id=block_side_id, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)


class BlockV1(Block):

    _bit_block_id_start = 0
    _bit_block_id_length = 11

    _bit_hit_points_start = 11
    _bit_hit_points_length = 9

    _bit_is_active_start = 20
    _bit_is_active_length = 1

    def __init__(self, int_24bit=0):
        super(BlockV1, self).__init__(int_24bit)

        self._int_24bit = int_24bit

        self._bit_block_id_start = 0
        self._bit_block_id_length = 11

        self._bit_hit_points_start = 11
        self._bit_hit_points_length = 9

        self._bit_is_active_start = 20
        self._bit_is_active_length = 1


class BlockV2(Block):

    _bit_block_id_start = 0
    _bit_block_id_length = 11

    _bit_hit_points_start = 11
    _bit_hit_points_length = 8

    _bit_is_active_start = 19
    _bit_is_active_length = 1

    def __init__(self, int_24bit=0):
        super(BlockV2, self).__init__(int_24bit)

        self._int_24bit = int_24bit

        self._bit_block_id_start = 0
        self._bit_block_id_length = 11

        self._bit_hit_points_start = 11
        self._bit_hit_points_length = 8

        self._bit_is_active_start = 19
        self._bit_is_active_length = 1


class BlockV3(Block):

    _bit_block_id_start = 0
    _bit_block_id_length = 11

    _bit_hit_points_start = 11
    _bit_hit_points_length = 7

    _bit_is_active_start = 18
    _bit_is_active_length = 1

    def __init__(self, int_24bit=0):
        super(BlockV3, self).__init__(int_24bit)

        self._int_24bit = int_24bit

        self._bit_block_id_start = 0
        self._bit_block_id_length = 11

        self._bit_hit_points_start = 11
        self._bit_hit_points_length = 7

        self._bit_is_active_start = 18
        self._bit_is_active_length = 1
